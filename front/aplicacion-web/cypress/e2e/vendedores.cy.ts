describe('Vendedor List', () => {
  beforeEach(() => {
    // Interceptar la petición HTTP de vendedores
    cy.intercept('GET', '**/vendedores', {
      statusCode: 200,
      body: [
        {
          id: '1',
          nombre: 'Juan Pérez',
          identificacion: '12345678',
          activo: true
        },
        {
          id: '2',
          nombre: 'María Rodríguez',
          identificacion: '87654321',
          activo: true
        },
        {
          id: '3',
          nombre: 'Carlos Gómez',
          identificacion: '98765432',
          activo: false
        }
      ]
    }).as('getVendedores');

    // Visitar la página
    cy.visit('/ventas/vendedores');
    
    // Esperar a que se complete la petición
    cy.wait('@getVendedores');
  });

  it('debe mostrar la lista de vendedores', () => {
    // Verificar que se muestran las tarjetas de vendedores
    cy.get('.card').should('have.length', 3);
    
    // Verificar que se muestra el nombre del primer vendedor
    cy.get('.card').first().should('contain', 'Juan Pérez');
    
    // Verificar que se muestra el ID del segundo vendedor
    cy.get('.card').eq(1).should('contain', '87654321');
  });

  it('debe navegar a la página de reportes al hacer clic en "Ver Reportes"', () => {
    // Interceptar la navegación
    cy.intercept('GET', '**/vendedores/1/reportes').as('getReportes');
    
    // Hacer clic en el botón "Ver Reportes" del primer vendedor
    cy.get('.card').first().contains('Ver Reportes').click();
    
    // Verificar que se navegó a la URL correcta
    cy.url().should('include', '/ventas/vendedor/1/reportes');
  });

  it('debe mostrar mensaje cuando no hay vendedores', () => {
    // Interceptar la petición HTTP con respuesta vacía
    cy.intercept('GET', '**/vendedores', {
      statusCode: 200,
      body: []
    }).as('getEmptyVendedores');
    
    // Recargar la página
    cy.visit('/ventas/vendedores');
    cy.wait('@getEmptyVendedores');
    
    // Verificar que se muestra el mensaje de "No hay vendedores"
    cy.contains('No hay vendedores registrados').should('be.visible');
  });

  it('debe manejar errores al cargar vendedores', () => {
    // Interceptar la petición HTTP con error
    cy.intercept('GET', '**/vendedores', {
      statusCode: 500,
      body: {
        message: 'Error interno del servidor'
      }
    }).as('getVendedoresError');
    
    // Recargar la página
    cy.visit('/ventas/vendedores');
    cy.wait('@getVendedoresError');
    
    // Verificar que se muestra el mensaje de error (ajusta esto según tu UI)
    cy.contains('Error al cargar vendedores').should('be.visible');
  });
});