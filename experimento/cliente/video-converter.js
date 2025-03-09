const fs = require('fs');
const path = require('path');

// Ruta a la carpeta de videos
const videoDir = path.join(__dirname, 'videos');
// Ruta para el archivo de salida
const outputFile = path.join(__dirname, 'video_data.js');

// Función para convertir un archivo a formato base64
function convertVideoToBase64(filePath) {
    try {
        // Leer el archivo binario
        const data = fs.readFileSync(filePath);
        // Convertir a base64
        const base64Data = data.toString('base64');
        return base64Data;
    } catch (error) {
        console.error(`Error al convertir ${filePath}: ${error.message}`);
        return null;
    }
}

// Función principal
async function main() {
    try {
        // Verificar si la carpeta de videos existe
        if (!fs.existsSync(videoDir)) {
            console.error(`La carpeta de videos no existe: ${videoDir}`);
            return;
        }

        console.log(`Procesando videos en: ${videoDir}`);

        // Leer todos los archivos en la carpeta
        const files = fs.readdirSync(videoDir);
        const videoFiles = files.filter(file => file.match(/^video\d+\.mp4$/));

        if (videoFiles.length === 0) {
            console.error('No se encontraron archivos de video con formato video{n}.mp4');
            return;
        }

        console.log(`Se encontraron ${videoFiles.length} archivos de video`);

        // Limitar a los primeros 10 videos para no crear un archivo demasiado grande
        // Puedes ajustar este número según tus necesidades
        const limitedVideoFiles = videoFiles.slice(0, 10);
        console.log(`Procesando los primeros ${limitedVideoFiles.length} videos`);

        // Objeto para almacenar los datos de los videos
        const videoData = {};

        // Procesar cada archivo
        for (const file of limitedVideoFiles) {
            const filePath = path.join(videoDir, file);
            console.log(`Procesando: ${file}`);

            const base64Data = convertVideoToBase64(filePath);
            if (base64Data) {
                const fileKey = path.basename(file, '.mp4'); // Extrae 'videoN' del nombre
                videoData[fileKey] = base64Data;
                console.log(`  ✓ Convertido: ${file} (${(base64Data.length / 1024 / 1024).toFixed(2)} MB)`);
            }
        }

        // Generar el archivo JavaScript
        const jsContent = `// Archivo generado automáticamente - Datos de videos en base64
export const videoData = ${JSON.stringify(videoData, null, 2)};
`;

        fs.writeFileSync(outputFile, jsContent);
        console.log(`\n✅ Se ha generado el archivo: ${outputFile}`);
        console.log(`   Tamaño del archivo: ${(fs.statSync(outputFile).size / 1024 / 1024).toFixed(2)} MB`);

    } catch (error) {
        console.error(`Error general: ${error.message}`);
    }
}

// Ejecutar la función principal
main();