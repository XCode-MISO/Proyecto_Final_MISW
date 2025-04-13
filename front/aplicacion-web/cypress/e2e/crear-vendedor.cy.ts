describe('Crear Vendedor', () => {
    it('debe registrar un nuevo vendedor', () => {
        cy.visit('ventas/vendedor/add');

        cy.get('input[formcontrolname="nombre"]').click({force: true}).type('Cypress Corp');
        cy.get('input[formcontrolname="correo"]').click({force: true}).type('cypress@correo.com');
        cy.get('input[formcontrolname="telefono"]').click({force: true}).type('12345678');
        cy.get('input[formcontrolname="direccion"]').click({force: true}).type('Calle 123# 1-25, Bogota, Colombia');

        cy.contains('Guardar').click();

        cy.get('p.mensaje')
            .scrollIntoView()
            .should('be.visible')
            .and('contain.text', 'Vendedor registrado correctamente');
    });
});

