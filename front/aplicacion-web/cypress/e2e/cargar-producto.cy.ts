describe('Cargar Producto', () => {
    it('debe registrar un nuevo producto correctamente', () => {
      cy.visit('/productos/crear');
  
      cy.get('input[formcontrolname="nombre"]').type('Producto Cypress');
      cy.get('mat-select[formcontrolname="fabricanteId"]').click();
      cy.get('mat-option').first().click();
      cy.get('input[formcontrolname="cantidad"]').type('5');
      cy.get('input[formcontrolname="precio"]').type('12.5');
      
      cy.get('form').submit();
      
      cy.get('p.mensaje', { timeout: 8000 })
        .should('exist')
        .and('contain.text', 'Producto cargado correctamente');
    });
  });

