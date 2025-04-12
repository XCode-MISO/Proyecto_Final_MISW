import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ProductosService, ProductoDto } from './productos.service';

describe('ProductosService', () => {
  let service: ProductosService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ProductosService]
    });
    service = TestBed.inject(ProductosService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); 
  });

  it('debe enviar un POST para cargar producto', () => {
    const productoMock: ProductoDto = {
      nombre: 'Producto de prueba',
      fabricanteId: 1,
      cantidad: 10,
      precio: 100
    };

    service.cargarProducto(productoMock).subscribe(response => {
      expect(response).toBeNull(); 
    });

    const req = httpMock.expectOne((req) =>
      req.method === 'POST' && req.url.includes('compras/detalle')
    );

    expect(req.request.body).toEqual(productoMock);
    req.flush(null); 
  });
});