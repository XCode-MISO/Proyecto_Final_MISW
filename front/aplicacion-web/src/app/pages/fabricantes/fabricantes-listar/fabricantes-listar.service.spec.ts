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
