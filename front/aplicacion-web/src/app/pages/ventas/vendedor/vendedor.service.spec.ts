import { TestBed } from '@angular/core/testing';

import { VendedorService } from './vendedor.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('VendedorAddService', () => {
  let service: VendedorService;

  beforeEach(() => {
    TestBed.configureTestingModule({imports:[HttpClientTestingModule]});
    service = TestBed.inject(VendedorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
