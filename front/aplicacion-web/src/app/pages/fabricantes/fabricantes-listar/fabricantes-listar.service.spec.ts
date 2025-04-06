import { TestBed } from '@angular/core/testing';
import { FabricantesListarService } from './fabricantes-listar.service';

describe('FabricantesListarService', () => {
  let service: FabricantesListarService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FabricantesListarService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
necesitoo crear el crear fabricante en el front como el mockup, Formulario de Registro:

Debe incluir los siguientes campos obligatorios:

Nombre (Texto, máximo 150 caracteres).

Correo (Debe ser una dirección de correo válida).

Teléfono (Debe contener solo números y tener entre 7 y 15 dígitos).

Empresa (Texto, máximo 150 caracteres).

Validaciones:

No se permite dejar campos vacíos.

Validación de formato en el correo electrónico.

El teléfono debe ser numérico y estar en un rango de 7 a 15 dígitos. voy a hacelo en angular, y necesito que tenga los archivos: 
 fabricantes-crear.component.html, fabricantes-crear.component.css, fabricantes-crear.component.ts, fabricantes-crear.component.service, fabricantes-crear.component.spec.ts, fabricantes-crear.service.spec.ts