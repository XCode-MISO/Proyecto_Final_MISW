import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Counter, Rate } from 'k6/metrics';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';
import encoding from 'k6/encoding';
import { videoData } from './video_data.js';

// Métricas
let processingTime = new Trend('processing_time');
let requestCounter = new Counter('requests_total');
let requestRate = new Rate('requests_rate');

// Configuración de control de tasa
const MAX_REQUESTS_PER_MINUTE = 60;  // Máximo permitido por la API
const SAFETY_FACTOR = 0.9;  // Factor de seguridad (90% del límite)
const ACTUAL_LIMIT = Math.floor(MAX_REQUESTS_PER_MINUTE * SAFETY_FACTOR);  // ~54 requests/minuto
const MIN_SLEEP_BETWEEN_REQUESTS = 60 / ACTUAL_LIMIT;  // Aprox. 1.11 segundos entre peticiones


let rateLimiter = {
    requestsThisMinute: 0,
    lastResetTime: 0,

    // Inicializar el limitador
    init() {
        this.lastResetTime = Date.now();
        this.requestsThisMinute = 0;
    },

    // Registrar una petición y dormir si es necesario
    async registerRequest() {
        const now = Date.now();

        // Si ha pasado un minuto, resetear el contador
        if (now - this.lastResetTime > 60000) {
            this.lastResetTime = now;
            this.requestsThisMinute = 0;
        }

        // Incrementar contador de peticiones
        this.requestsThisMinute++;

        // Si estamos cerca del límite, esperar proporcionalmente
        if (this.requestsThisMinute >= ACTUAL_LIMIT) {
            const timeToNextMinute = 60000 - (now - this.lastResetTime);
            console.log(`Alcanzado límite de ${ACTUAL_LIMIT} peticiones por minuto. Esperando ${timeToNextMinute/1000} segundos.`);
            sleep(timeToNextMinute / 1000); // Convertir a segundos para sleep
            this.lastResetTime = Date.now();
            this.requestsThisMinute = 0;
        } else {
            // Siempre esperamos un mínimo entre peticiones para mantener la tasa
            sleep(MIN_SLEEP_BETWEEN_REQUESTS);
        }
    }
};

// Configuración de la prueba
export let options = {
    vus: 3,           // Reducido el número de usuarios virtuales concurrentes
    iterations: 10,   // Reducido el número de iteraciones
    // No usamos duración fija para tener más control sobre el número total de peticiones
};

// Función principal
export function setup() {
    rateLimiter.init();
    console.log(`Configuración: Máximo ${ACTUAL_LIMIT} peticiones por minuto (${MIN_SLEEP_BETWEEN_REQUESTS.toFixed(2)}s entre peticiones)`);
    return { startTime: Date.now() };
}

export default function (data) {
    // Obtener las claves (nombres de videos) disponibles
    const videoKeys = Object.keys(videoData);

    if (videoKeys.length === 0) {
        console.error('No hay datos de video disponibles');
        return;
    }

    // Elegir un video aleatorio de los disponibles
    const randomIndex = randomIntBetween(0, videoKeys.length - 1);
    const videoKey = videoKeys[randomIndex];
    const fileName = `${videoKey}.mp4`;

    try {
        // Obtener los datos base64 del video y decodificarlos
        const base64Data = videoData[videoKey];
        const binaryData = encoding.b64decode(base64Data);

        console.log(`Usando video real: ${fileName} (${(binaryData.length / 1024).toFixed(2)} KB)`);

        // Esperar si es necesario antes de hacer la petición
        rateLimiter.registerRequest();

        // Construimos el multipart form para subir
        let formData = {
            video: http.file(binaryData, fileName, 'video/mp4'),
        };

        // Paso 1: Subida del video al microservicio Command
        let uploadStart = new Date().getTime();
        let uploadRes = http.post('http://34.60.201.251/command/api/upload', formData);
        let uploadEnd = new Date().getTime();
        let uploadTime = (uploadEnd - uploadStart) / 1000;

        // Registrar métricas
        requestCounter.add(1);
        requestRate.add(1);

        console.log(`Tiempo de subida: ${uploadTime.toFixed(2)} segundos`);

        check(uploadRes, {
            'upload success': (r) => r.status === 201 && r.json('job_id') !== undefined,
        });

        if (uploadRes.status > 300) {
            console.log(`Error en la subida: ${uploadRes.status}, Respuesta: ${uploadRes.body}`);
            return;
        }

        let jobId;
        try {
            jobId = uploadRes.json('job_id');
            if (!jobId) {
                console.log(`No se obtuvo jobId, respuesta: ${uploadRes.body}`);
                return;
            }
        } catch (e) {
            console.log(`Error al procesar respuesta JSON: ${e.message}, Cuerpo: ${uploadRes.body}`);
            return;
        }

        console.log(`Subida exitosa, jobId: ${jobId}`);

        // Se inicia el tiempo crítico a partir de que se recibe el jobID
        let startTime = new Date().getTime();

        // Paso 2: Polling del estado del procesamiento
        let processed = false;
        let maxAttempts = 30; // Reducido para limitar el número de peticiones
        let attempts = 0;

        while (!processed && attempts < maxAttempts) {


            // Esperar si es necesario antes de hacer la petición
            rateLimiter.registerRequest();

            attempts++;
            let statusUrl = `http://34.60.201.251/query/api/recommend?job_id=${jobId}`;

            let statusRes = http.get(statusUrl);

            // Registrar métricas
            requestCounter.add(1);
            requestRate.add(1);

            if (statusRes.status === 200) {
                try {
                    let jsonResponse = JSON.parse(statusRes.body);

                    if (jsonResponse.state === 'processed') {
                        processed = true;
                        console.log(`Video procesado después de ${attempts} intentos`);
                    } else {
                        console.log(`Estado actual: ${jsonResponse.state || 'desconocido'}`);
                    }
                } catch (e) {
                    console.log(`Error al parsear JSON: ${e.message}, Respuesta: ${statusRes.body}`);
                }
            } else {
                console.log(`Estado HTTP inesperado: ${statusRes.status}, Respuesta: ${statusRes.body}`);
            }

            if (!processed) {
                // No es necesario sleep adicional aquí, ya que rateLimiter.registerRequest ya incluye sleep
            }
        }

        if (!processed) {
            console.log(`No se completó el procesamiento después de ${maxAttempts} intentos para el jobId: ${jobId}`);
            return;
        }

        let endTime = new Date().getTime();
        let totalProcessingTime = (endTime - startTime) / 1000; // en segundos
        processingTime.add(totalProcessingTime);
        console.log(`Procesamiento completado en ${totalProcessingTime.toFixed(2)} segundos`);
    } catch (error) {
        console.error(`Error general en la iteración con video ${fileName}: ${error.message}`);
    }
}

export function teardown(data) {
    const testDuration = (Date.now() - data.startTime) / 1000;
    console.log(`Prueba completada en ${testDuration.toFixed(2)} segundos.`);
    console.log(`Tasa de peticiones promedio: ${(requestCounter.count / (testDuration / 60)).toFixed(2)} req/min`);
}