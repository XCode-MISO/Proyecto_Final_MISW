import { TestBed } from '@angular/core/testing';
import { FabricantesListarService } from './fabricantes-listar.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideNativeDateAdapter } from '@angular/material/core';

describe('FabricantesListarService', () => {
  let service: FabricantesListarService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        provideNativeDateAdapter()
      ]
    });
    service = TestBed.inject(FabricantesListarService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});