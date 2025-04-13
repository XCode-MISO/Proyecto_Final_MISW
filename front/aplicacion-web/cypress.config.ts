import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'https://website.cppxcode.shop/',
    specPattern: 'cypress/e2e/**/*.cy.ts',
    supportFile: false
  }
})