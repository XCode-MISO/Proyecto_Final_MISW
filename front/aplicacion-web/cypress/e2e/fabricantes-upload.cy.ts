describe('Carga Masiva de Fabricantes', () => {
    beforeEach(() => {
      cy.visit('/fabricantes/menu');
  

      cy.get('#btn-seleccion-carga').click();
      cy.url().should('include', '/fabricantes/seleccion-carga');
  
    
      cy.get('#btn-carga-masiva').click();
      cy.url().should('include', '/fabricantes/upload');
    });
  
    it('debería permitir subir un CSV y mostrar mensaje de éxito', () => {
    
      cy.get('input[type="file"]').should('be.visible');
  
      const csvContent = "nombre,correo,telefono,empresa\nFabricante A,contactoA@example.com,1234567,Empresa A";
  
      cy.get('input[type="file"]').attachFile({
        fileContent: csvContent,
        fileName: 'fabricantes.csv',
        mimeType: 'text/csv'
      });
  
      cy.get('.loading', { timeout: 10000 }).should('be.visible');
  
      cy.get('.response-message', { timeout: 15000 }).should('contain', 'Carga exitosa');
  
      cy.get('.error-messages').should('not.exist');
    });
  
    it('debería mostrar errores si el CSV tiene filas incompletas', () => {
      const csvContent =
        "nombre,correo,telefono,empresa\n" +
        "Fabricante A,contactoA@example.com,1234567,Empresa A\n" +
        "Fabricante B,,7654321,Empresa B";
  
      cy.get('input[type="file"]').attachFile({
        fileContent: csvContent,
        fileName: 'fabricantes_error.csv',
        mimeType: 'text/csv'
      });
  
      cy.get('.error-messages', { timeout: 15000 })
        .should('be.visible')
        .and('contain', 'Falta(s) campo(s)');
    });
  });