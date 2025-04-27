describe('Pruebas de confidencialidad según rol', () => {
  // Esta función realizará el login con un usuario específico
  function loginWithUser(userType) {
    cy.fixture('users.json').then((users) => {
      const user = users[userType];
      
      // Configurar un tiempo de espera más largo para la carga de la página
      cy.visit('/login', { timeout: 30000 });
      
      // Esperar a que el formulario de login esté visible y HABILITADO
      cy.get('[data-cy="login-email"]', { timeout: 10000 })
        .should('be.visible')
        .should('not.be.disabled');
      
      // Romper el encadenamiento usando aliases
      cy.get('[data-cy="login-email"]').as('emailField');
      cy.get('@emailField').click();
      cy.get('@emailField').clear();
      // Esperar un momento para que Angular procese el clear
      cy.wait(300);
      cy.get('@emailField').type(user.email, { force: true });
      
      // Lo mismo para la contraseña
      cy.get('[data-cy="login-password"]')
        .should('be.visible')
        .should('not.be.disabled')
        .as('passwordField');
      
      cy.get('@passwordField').click();
      cy.get('@passwordField').clear();
      // Esperar un momento
      cy.wait(300);
      cy.get('@passwordField').type(user.password, { force: true });
      
      // Esperar que el botón de envío esté habilitado
      cy.get('[data-cy="login-submit"]')
        .should('be.visible')
        .should('not.be.disabled')
        .click();
      
      // El resto de la prueba...
      cy.url({ timeout: 10000 }).should('include', '/home');
      
      cy.contains('Salir', { timeout: 10000 }).should('be.visible');
      cy.wait(1000);
      
      user.expectedMenus.forEach(menu => {
        cy.contains(menu, { timeout: 5000 }).should('be.visible');
      });
      
      user.unexpectedMenus.forEach(menu => {
        cy.contains(menu).should('not.exist');
      });
      
      cy.contains('Salir').click();
      cy.url().should('include', '/login');
    });
  }

  it('Administrador debería ver todos los menús', () => {
    loginWithUser('admin');
  });

  it('Director de Ventas debería ver solo sus menús correspondientes', () => {
    loginWithUser('directorVentas');
  });

  it('Director de Compras debería ver solo sus menús correspondientes', () => {
    loginWithUser('directorCompras');
  });

  it('Director de Logística debería ver solo sus menús correspondientes', () => {
    loginWithUser('directorLogistica');
  });
});