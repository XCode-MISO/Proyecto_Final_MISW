import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ProductosUploadService } from './productos-upload.service';
import { environment } from '../../../../environments/environment';

describe('ProductosUploadService', () => {
  let service: ProductosUploadService;
  let httpMock: HttpTestingController;
  const dummyResponse = { inserted: 2, errors: [] };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ProductosUploadService]
    });
    service = TestBed.inject(ProductosUploadService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('debería subir archivo y retornar respuesta exitosa', () => {
    const formData = new FormData();
    formData.append('file', new Blob(["dummy content"], { type: 'text/csv' }), 'Productos.csv');

    service.uploadFile(formData).subscribe(response => {
      expect(response.inserted).toEqual(2);
      expect(response.errors.length).toEqual(0);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/api/Productos/upload`);
    expect(req.request.method).toBe('POST');
    req.flush(dummyResponse);
  });
});