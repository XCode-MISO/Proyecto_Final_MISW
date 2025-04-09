import { TestBed } from '@angular/core/testing';

import { VendedorAddService } from './vendedor-add.service';

describe('VendedorAddService', () => {
  let service: VendedorAddService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VendedorAddService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
