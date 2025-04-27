// ***********************************************************
// This example support/e2e.ts is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands';

// Alternatively you can use CommonJS syntax:
// require('./commands')

// Soporte para estadísticas de confidencialidad
declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Inicializa las estadísticas de confidencialidad
       */
      initConfidentialityStats(): Chainable<void>;
      
      /**
       * Registra un intento de acceso a una URL restringida
       * @param role El rol que intenta acceder (directorVentas, directorCompras, directorLogistica)
       * @param resource El recurso al que se intenta acceder (fabricantes, ventas, routes, etc.)
       * @param isAccessDenied Si el acceso fue denegado correctamente
       */
      recordAccessAttempt(role: string, resource: string, isAccessDenied: boolean): Chainable<void>;
      
      /**
       * Registra el resultado de una prueba de confidencialidad
       * @param role El rol que se está probando
       * @param testType El tipo de prueba que se está realizando
       * @param isPassing Si la prueba ha pasado o no
       */
      recordConfidentialityTest(role: string, testType: string, isPassing: boolean): Chainable<void>;
      
      /**
       * Genera un reporte de confidencialidad basado en las estadísticas recopiladas
       */
      generateConfidentialityReport(): Chainable<void>;
    }
  }
}

// Estadísticas de confidencialidad
interface ConfidentialityStats {
  accessAttempts: {
    total: number;
    denied: number;
    byRole: Record<string, {
      attempted: number;
      denied: number;
      resources: Record<string, {
        attempted: number;
        denied: number;
      }>;
    }>;
  };
  generalTests: {
    total: number;
    passed: number;
    byRole: Record<string, {
      total: number;
      passed: number;
      byType: Record<string, {
        total: number;
        passed: number;
      }>;
    }>;
  };
}

// Inicializar estadísticas
let confidentialityStats: ConfidentialityStats = {
  accessAttempts: {
    total: 0,
    denied: 0,
    byRole: {}
  },
  generalTests: {
    total: 0,
    passed: 0,
    byRole: {}
  }
};

// Comandos personalizados para estadísticas de confidencialidad
Cypress.Commands.add('initConfidentialityStats', () => {
  confidentialityStats = {
    accessAttempts: {
      total: 0,
      denied: 0,
      byRole: {}
    },
    generalTests: {
      total: 0,
      passed: 0,
      byRole: {}
    }
  };
  
  // Roles iniciales
  const roles = ['admin', 'directorVentas', 'directorCompras', 'directorLogistica'];
  roles.forEach(role => {
    confidentialityStats.accessAttempts.byRole[role] = {
      attempted: 0,
      denied: 0,
      resources: {}
    };
    
    confidentialityStats.generalTests.byRole[role] = {
      total: 0,
      passed: 0,
      byType: {}
    };
  });
  
  cy.log('Estadísticas de confidencialidad inicializadas');
});

Cypress.Commands.add('recordAccessAttempt', (role, resource, isAccessDenied) => {
  // Incrementar contadores globales
  confidentialityStats.accessAttempts.total++;
  if (isAccessDenied) {
    confidentialityStats.accessAttempts.denied++;
  }
  
  // Asegurarse de que exista la estructura para el rol
  if (!confidentialityStats.accessAttempts.byRole[role]) {
    confidentialityStats.accessAttempts.byRole[role] = {
      attempted: 0,
      denied: 0,
      resources: {}
    };
  }
  
  // Incrementar contadores del rol
  confidentialityStats.accessAttempts.byRole[role].attempted++;
  if (isAccessDenied) {
    confidentialityStats.accessAttempts.byRole[role].denied++;
  }
  
  // Asegurarse de que exista la estructura para el recurso
  if (!confidentialityStats.accessAttempts.byRole[role].resources[resource]) {
    confidentialityStats.accessAttempts.byRole[role].resources[resource] = {
      attempted: 0,
      denied: 0
    };
  }
  
  // Incrementar contadores del recurso
  confidentialityStats.accessAttempts.byRole[role].resources[resource].attempted++;
  if (isAccessDenied) {
    confidentialityStats.accessAttempts.byRole[role].resources[resource].denied++;
  }
  
  cy.log(`Acceso para ${role} a ${resource}: ${isAccessDenied ? 'Denegado ✓' : 'Permitido ✗'}`);
});

Cypress.Commands.add('recordConfidentialityTest', (role, testType, isPassing) => {
  // Incrementar contadores globales
  confidentialityStats.generalTests.total++;
  if (isPassing) {
    confidentialityStats.generalTests.passed++;
  }
  
  // Asegurarse de que exista la estructura para el rol
  if (!confidentialityStats.generalTests.byRole[role]) {
    confidentialityStats.generalTests.byRole[role] = {
      total: 0,
      passed: 0,
      byType: {}
    };
  }
  
  // Incrementar contadores del rol
  confidentialityStats.generalTests.byRole[role].total++;
  if (isPassing) {
    confidentialityStats.generalTests.byRole[role].passed++;
  }
  
  // Asegurarse de que exista la estructura para el tipo de prueba
  if (!confidentialityStats.generalTests.byRole[role].byType[testType]) {
    confidentialityStats.generalTests.byRole[role].byType[testType] = {
      total: 0,
      passed: 0
    };
  }
  
  // Incrementar contadores del tipo de prueba
  confidentialityStats.generalTests.byRole[role].byType[testType].total++;
  if (isPassing) {
    confidentialityStats.generalTests.byRole[role].byType[testType].passed++;
  }
  
  cy.log(`Prueba ${testType} para ${role}: ${isPassing ? 'Pasó ✓' : 'Falló ✗'}`);
});

Cypress.Commands.add('generateConfidentialityReport', () => {
  // Calcular tasas de éxito
  const accessSuccessRate = (confidentialityStats.accessAttempts.denied / confidentialityStats.accessAttempts.total * 100).toFixed(2);
  const testSuccessRate = (confidentialityStats.generalTests.passed / confidentialityStats.generalTests.total * 100).toFixed(2);
  
  // Generar reporte en la consola
  cy.log('===== REPORTE DE CONFIDENCIALIDAD =====');
  cy.log(`Tasa de éxito en control de acceso: ${accessSuccessRate}%`);
  cy.log(`Tasa de éxito en pruebas generales: ${testSuccessRate}%`);
  cy.log(`Intentos de acceso total: ${confidentialityStats.accessAttempts.total}`);
  cy.log(`Accesos denegados correctamente: ${confidentialityStats.accessAttempts.denied}`);
  
  // Detalles por rol
  Object.keys(confidentialityStats.accessAttempts.byRole).forEach(role => {
    const roleStats = confidentialityStats.accessAttempts.byRole[role];
    if (roleStats.attempted > 0) {
      const roleSuccessRate = (roleStats.denied / roleStats.attempted * 100).toFixed(2);
      cy.log(`${role}: ${roleSuccessRate}% (${roleStats.denied}/${roleStats.attempted})`);
    }
  });
  
  // Guardar el reporte como archivo JSON para procesamiento posterior
  cy.task('writeConfidentialityReport', {
    stats: confidentialityStats,
    timestamp: new Date().toISOString()
  });
});