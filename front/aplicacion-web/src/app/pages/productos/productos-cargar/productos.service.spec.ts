import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ProductosService, ProductoDto } from './productos.service';

describe('ProductosService', () => {
  let service: ProductosService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(ProductosService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('should POST producto', () => {
    const prod: ProductoDto = { nombre: 'P', fabricanteId: 1, cantidad: 5, precio: 3 };

    service.cargarProducto(prod).subscribe();

    const req = httpMock.expectOne('/api/compras/detalle');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(prod);
    req.flush(null);
  });
});