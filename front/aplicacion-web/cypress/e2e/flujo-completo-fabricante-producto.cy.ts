describe('Flujo completo: crear fabricante + cargar producto', () => {
    const nombreFabricante = 'Fabricante Cypress ' + Date.now();
    const nombreProducto = 'Producto Cypress';
  
    it('debe crear un fabricante y luego usarlo para registrar un producto', () => {
      // 1. Crear fabricante
      cy.visit('/fabricantes/crear');
  
      cy.get('input[formcontrolname="nombre"]').type(nombreFabricante);
      cy.get('input[formcontrolname="correo"]').type('fabricante@cypress.com');
      cy.get('input[formcontrolname="telefono"]').type('12345678');
      cy.get('input[formcontrolname="empresa"]').type('Empresa Cypress');
  
      cy.contains('Guardar').click();
  
      cy.get('p.mensaje', { timeout: 8000 })
        .should('contain.text', 'Fabricante registrado correctamente');
  
      // 2. Ir a cargar producto
      cy.visit('/productos/crear');
  
      cy.get('input[formcontrolname="nombre"]').type(nombreProducto);
  
      // 3. Seleccionar fabricante recién creado
      cy.get('mat-select[formcontrolname="fabricanteId"]').click();
  
      cy.get('mat-option').contains(nombreFabricante).click();
  
      // 4. Ingresar cantidad y precio
      cy.get('input[formcontrolname="cantidad"]').type('10');
      cy.get('input[formcontrolname="precio"]').type('99.99');
  
      cy.get('form').submit();
  
      // 5. Validar éxito
      cy.get('p.mensaje', { timeout: 8000 })
        .should('contain.text', 'Producto cargado correctamente');
    });
  });