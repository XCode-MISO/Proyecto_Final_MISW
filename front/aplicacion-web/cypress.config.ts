import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:4200',
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 120000, // Aumentar el tiempo de espera para carga de páginas
    video: false,
    chromeWebSecurity: false,
    setupNodeEvents(on, config) {
      // implementar configuración de eventos si es necesario
    },
  },
})