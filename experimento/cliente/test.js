import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Counter, Rate } from 'k6/metrics';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';
import encoding from 'k6/encoding';
import { videoData } from './video_data.js';

// Configuración de control de tasa
const MAX_REQUESTS_PER_MINUTE = 120;  // Máximo permitido por la API
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
            //console.log(`Alcanzado límite de ${ACTUAL_LIMIT} peticiones por minuto. Esperando ${timeToNextMinute/1000} segundos.`);
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
    scenarios: {
        subirYRevisarVideos: {
            executor: 'constant-arrival-rate',

            // How long the test lasts
            duration: '30m',

            // How many iterations per timeUnit
            rate: 20,

            // Start `rate` iterations per second
            timeUnit: '1m',

            // Pre-allocate 2 VUs before starting the test
            preAllocatedVUs: 100,

            // Spin up a maximum of 50 VUs to sustain the defined
            // constant arrival rate.
            maxVUs: 120,
        },
    },
};

// Función principal
export function setup() {
    rateLimiter.init();
    //console.log(`Configuración: Máximo ${ACTUAL_LIMIT} peticiones por minuto (${MIN_SLEEP_BETWEEN_REQUESTS.toFixed(2)}s entre peticiones)`);
    return { startTime: Date.now() };
}


// Métricas
let processingTime = new Trend('processing_time');
let requestCounter = new Counter('requests_total');
let requestRate = new Rate('requests_rate');

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

        //console.log(`Usando video real: ${fileName} (${(binaryData.length / 1024).toFixed(2)} KB)`);

        // Esperar si es necesario antes de hacer la petición
        rateLimiter.registerRequest();

        // Construimos el multipart form para subir
        let formData = {
            video: http.file(binaryData, fileName, 'video/mp4'),
        };

        // Paso 1: Subida del video al microservicio Command
        let uploadStart = new Date().getTime();
        let uploadRes = http.post('https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/upload', formData, 
        {
          headers: {
            Authorization: "Bearer <token>"
          }
        });
        let uploadEnd = new Date().getTime();
        let uploadTime = (uploadEnd - uploadStart) / 1000;

        // Registrar métricas
        requestCounter.add(1);
        requestRate.add(1);

        //console.log(`Tiempo de subida: ${uploadTime.toFixed(2)} segundos`);

        check(uploadRes, {
            'upload success': (r) => r.status === 201 && r.json('job_id') !== undefined,
        });

        if (uploadRes.status > 300) {
            //console.log(`Error en la subida: ${uploadRes.status}, Respuesta: ${uploadRes.body}`);
            return;
        }

        let jobId;
        try {
            jobId = uploadRes.json('job_id');
            if (!jobId) {
                //console.log(`No se obtuvo jobId, respuesta: ${uploadRes.body}`);
                return;
            }
        } catch (e) {
            //console.log(`Error al procesar respuesta JSON: ${e.message}, Cuerpo: ${uploadRes.body}`);
            return;
        }

        //console.log(`Subida exitosa, jobId: ${jobId}`);

        // Se inicia el tiempo crítico a partir de que se recibe el jobID
        let startTime = new Date().getTime();

        // Paso 2: Polling del estado del procesamiento
        let processed = false;
        let maxAttempts = 30; // Reducido para limitar el número de peticiones
        let attempts = 0;
        // Esperar si es necesario antes de hacer la petición
        rateLimiter.registerRequest();
        // Registrar métricas
        requestCounter.add(1);
        requestRate.add(1);

        let interval

        const timeout = setTimeout(() => {
            if (interval) {
                console.log(`Limpiando interavlo por fuera del ciclo: no se obtuvo una respuesta a tiempo`)
                processed = true
                clearInterval(interval)
                clearTimeout(timeout)
            }
        }, 20000)


        interval = setInterval(() => {
            if (processed) {
                console.log("clear interval inside itself")
                clearInterval(interval)
            }

            attempts++;
            let statusUrl = `https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/recommend?job_id=${jobId}`;

            let statusRes = http.get(statusUrl, 
                {
                  headers: {
                    Authorization: "Bearer <token>"
                  }
                });

            if (statusRes.status === 200) {
                try {
                    let jsonResponse = JSON.parse(statusRes.body);
                    console.log(jsonResponse)

                    if (jsonResponse.final_state === 'processed') {
                        processed = true;
                        let endTime = new Date().getTime();
                        let totalProcessingTime = (endTime - startTime) / 1000; // en segundos
                        processingTime.add(totalProcessingTime);
                        clearInterval(interval)
                        clearTimeout(timeout)
                        console.log(`Video procesado después de ${attempts} intentos`);
                    } else {
                        //console.log(`Estado actual: ${jsonResponse.state || 'desconocido'}`);
                    }
                } catch (e) {
                    //console.log(`Error al parsear JSON: ${e.message}, Respuesta: ${statusRes.body}`);
                }
            }
            if (statusRes.status === 404) {
                //console.log(`Estado HTTP 404: ${statusRes.status}, Respuesta: ${statusRes.body}`);
            }
        }, 500)

        check(processed, Boolean)

    } catch (error) {
        console.error(`Error general en la iteración con video ${fileName}: ${error.message}`);
    }
}

export function teardown(data) {
    const testDuration = (Date.now() - data.startTime) / 1000;
    //console.log(`Prueba completada en ${testDuration.toFixed(2)} segundos.`);
    //console.log(`Tasa de peticiones promedio: ${(requestCounter.count / (testDuration / 60)).toFixed(2)} req/min`);
}