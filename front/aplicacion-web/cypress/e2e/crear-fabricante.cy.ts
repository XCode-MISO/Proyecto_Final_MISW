describe('Crear Fabricante', () => {
    it('debe registrar un nuevo fabricante', () => {
        cy.visit('/fabricantes/crear');

        cy.get('input[formcontrolname="nombre"]').type('Cypress Corp');
        cy.get('input[formcontrolname="correo"]').type('cypress@correo.com');
        cy.get('input[formcontrolname="telefono"]').type('12345678');
        cy.get('input[formcontrolname="empresa"]').type('Cypress Testing');

        cy.contains('Guardar').click();

        cy.get('p.mensaje')
            .scrollIntoView()
            .should('be.visible')
            .and('contain.text', 'Fabricante registrado correctamente');
    });
});

