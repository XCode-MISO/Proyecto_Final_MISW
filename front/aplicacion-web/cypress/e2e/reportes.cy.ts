describe('Vendedor Reportes', () => {
  beforeEach(() => {
    // Interceptar la petición HTTP de datos del vendedor
    cy.intercept('GET', '**/vendedores/1', {
      statusCode: 200,
      body: {
        id: '1',
        nombre: 'Juan Pérez',
        identificacion: '12345678',
        activo: true
      }
    }).as('getVendedor');
    
    // Interceptar la petición HTTP de reportes
    cy.intercept('GET', '**/vendedores/1/reportes', {
      statusCode: 200,
      body: {
        vendedor_id: '1',
        reportes: [
          {
            id: '101',
            fecha: '2025-05-10',
            producto: 'Smartphone Galaxy S25',
            cantidad: 3
          },
          {
            id: '102',
            fecha: '2025-05-15',
            producto: 'Laptop ProBook X1',
            cantidad: 1
          }
        ]
      }
    }).as('getReportes');

    // Visitar la página de reportes
    cy.visit('/ventas/vendedor/1/reportes');
    
    // Esperar a que se completen las peticiones
    cy.wait(['@getVendedor', '@getReportes']);
  });

  it('debe mostrar el nombre del vendedor', () => {
    cy.get('.vendor-name').should('contain', 'Juan Pérez');
  });

  it('debe mostrar la tabla de reportes con datos', () => {
    // Verificar que la tabla existe
    cy.get('table').should('be.visible');
    
    // Verificar número de filas (2 reportes + fila de encabezado)
    cy.get('tr').should('have.length', 3);
    
    // Verificar contenido de las celdas
    cy.get('tr').eq(1).find('td').eq(1).should('contain', 'Smartphone Galaxy S25');
    cy.get('tr').eq(2).find('td').eq(2).should('contain', '1');
  });

  it('debe mostrar mensaje cuando no hay reportes', () => {
    // Interceptar con respuesta vacía
    cy.intercept('GET', '**/vendedores/1/reportes', {
      statusCode: 200,
      body: {
        vendedor_id: '1',
        reportes: []
      }
    }).as('getEmptyReportes');
    
    // Recargar la página
    cy.visit('/ventas/vendedor/1/reportes');
    cy.wait(['@getVendedor', '@getEmptyReportes']);
    
    // Verificar mensaje
    cy.contains('No se encontraron reportes').should('be.visible');
  });
});