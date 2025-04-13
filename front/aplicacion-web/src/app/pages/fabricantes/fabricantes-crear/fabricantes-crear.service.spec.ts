import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FabricantesCrearService } from './fabricantes-crear.service';
import { environment } from '../../../../environments/environment';

interface Fabricante {
  nombre: string;
  correo: string;
  telefono: string;
  empresa: string;
}

describe('FabricantesCrearService', () => {
  let service: FabricantesCrearService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(FabricantesCrearService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should POST and return fabricante', () => {
    const mockFabricante: Fabricante = {
      nombre: 'Prueba',
      correo: 'prueba@correo.com',
      telefono: '1234567',
      empresa: 'Empresa Prueba'
    };

    service.crearFabricante(mockFabricante).subscribe(resp => {
      expect(resp).toEqual(mockFabricante);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/api/fabricantes`);
    expect(req.request.method).toBe('POST');
    req.flush(mockFabricante);
  });
});