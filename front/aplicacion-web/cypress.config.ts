import { defineConfig } from 'cypress';
import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      on('task', {
        // Tarea para escribir el reporte de confidencialidad
        writeConfidentialityReport({ stats, timestamp }) {
          // Crear directorio de reportes si no existe
          const reportsDir = join(__dirname, 'cypress', 'reports');
          if (!existsSync(reportsDir)) {
            mkdirSync(reportsDir, { recursive: true });
          }
          
          // Guardar reporte JSON
          const jsonPath = join(reportsDir, 'confidentiality-report.json');
          writeFileSync(jsonPath, JSON.stringify(stats, null, 2));
          
          // Generar reporte HTML
          const accessSuccessRate = (stats.accessAttempts.denied / stats.accessAttempts.total * 100).toFixed(2);
          const testSuccessRate = (stats.generalTests.passed / stats.generalTests.total * 100).toFixed(2);
          
          const html = `
            <!DOCTYPE html>
            <html>
            <head>
              <title>Reporte de Confidencialidad</title>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background-color: #0275d8; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
                .card { background-color: white; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 20px; margin-bottom: 20px; }
                h1, h2, h3 { margin-top: 0; }
                .metrics { display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }
                .metric { flex: 1; min-width: 200px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }
                .metric-value { font-size: 24px; font-weight: bold; margin: 10px 0; }
                .success { color: #28a745; }
                .warning { color: #ffc107; }
                .danger { color: #dc3545; }
                .neutral { color: #0275d8; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                .progress-container { width: 100%; background-color: #f1f1f1; border-radius: 5px; }
                .progress-bar { height: 24px; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; }
                .timestamp { text-align: right; color: #666; font-size: 14px; margin-top: 30px; }
              </style>
            </head>
            <body>
              <div class="container">
                <div class="header">
                  <h1>Reporte de Confidencialidad</h1>
                  <p>Resultados de pruebas de seguridad y control de acceso</p>
                </div>
                
                <div class="card">
                  <h2>Resumen Ejecutivo</h2>
                  <div class="metrics">
                    <div class="metric">
                      <h3>Control de Acceso</h3>
                      <div class="metric-value ${getColorClass(parseFloat(accessSuccessRate))}">${accessSuccessRate}%</div>
                      <p>Tasa de éxito</p>
                    </div>
                    <div class="metric">
                      <h3>Pruebas Generales</h3>
                      <div class="metric-value ${getColorClass(parseFloat(testSuccessRate))}">${testSuccessRate}%</div>
                      <p>Tasa de éxito</p>
                    </div>
                    <div class="metric">
                      <h3>Total Pruebas</h3>
                      <div class="metric-value neutral">${stats.accessAttempts.total + stats.generalTests.total}</div>
                      <p>Pruebas ejecutadas</p>
                    </div>
                  </div>
                </div>
                
                <div class="card">
                  <h2>Control de Acceso por Rol</h2>
                  <table>
                    <tr>
                      <th>Rol</th>
                      <th>Intentos</th>
                      <th>Denegados</th>
                      <th>Tasa de Éxito</th>
                      <th>Progreso</th>
                    </tr>
                    ${Object.keys(stats.accessAttempts.byRole).map(role => {
                      const roleStats = stats.accessAttempts.byRole[role];
                      if (roleStats.attempted === 0) return '';
                      const successRate = (roleStats.denied / roleStats.attempted * 100).toFixed(2);
                      return `
                        <tr>
                          <td>${role}</td>
                          <td>${roleStats.attempted}</td>
                          <td>${roleStats.denied}</td>
                          <td>${successRate}%</td>
                          <td>
                            <div class="progress-container">
                              <div class="progress-bar ${getColorClass(parseFloat(successRate))}" 
                                   style="width: ${successRate}%">
                                ${successRate}%
                              </div>
                            </div>
                          </td>
                        </tr>
                      `;
                    }).join('')}
                  </table>
                </div>
                
                <div class="card">
                  <h2>Detalle por Recursos</h2>
                  ${Object.keys(stats.accessAttempts.byRole).map(role => {
                    const roleResources = stats.accessAttempts.byRole[role].resources;
                    if (Object.keys(roleResources).length === 0) return '';
                    
                    return `
                      <h3>${role}</h3>
                      <table>
                        <tr>
                          <th>Recurso</th>
                          <th>Intentos</th>
                          <th>Denegados</th>
                          <th>Tasa de Éxito</th>
                        </tr>
                        ${Object.keys(roleResources).map(resource => {
                          const resourceStats = roleResources[resource];
                          const successRate = (resourceStats.denied / resourceStats.attempted * 100).toFixed(2);
                          return `
                            <tr>
                              <td>${resource}</td>
                              <td>${resourceStats.attempted}</td>
                              <td>${resourceStats.denied}</td>
                              <td class="${getColorClass(parseFloat(successRate))}">${successRate}%</td>
                            </tr>
                          `;
                        }).join('')}
                      </table>
                    `;
                  }).join('')}
                </div>
                
                <div class="timestamp">
                  Generado el ${new Date(timestamp).toLocaleString()}
                </div>
              </div>
            </body>
            </html>
          `;
          
          // Función para determinar la clase de color según el porcentaje
          function getColorClass(percent) {
            if (percent >= 90) return 'success';
            if (percent >= 75) return 'warning';
            return 'danger';
          }
          
          // Guardar reporte HTML
          const htmlPath = join(reportsDir, 'confidentiality-report.html');
          writeFileSync(htmlPath, html);
          
          console.log(`Reporte de confidencialidad generado en: ${reportsDir}`);
          console.log(`- JSON: confidentiality-report.json`);
          console.log(`- HTML: confidentiality-report.html`);
          
          return true;
        }
      });
      
      // Configuración para Mochawesome Reporter
      require('cypress-mochawesome-reporter/plugin')(on);
    },
    baseUrl: 'http://localhost:4200',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    video: false
  },
  
  // Configuración del reporter
  reporter: 'cypress-mochawesome-reporter',
  reporterOptions: {
    charts: true,
    reportPageTitle: 'Reporte de Pruebas - Confidencialidad',
    embeddedScreenshots: true,
    inlineAssets: true,
    saveAllAttempts: false,
  },
  
  // Configuraciones generales
  viewportWidth: 1280,
  viewportHeight: 720,
  defaultCommandTimeout: 10000
});npx cypress run --spec "cypress/e2e/auth/pruebas-confidencialidad.cy.ts"