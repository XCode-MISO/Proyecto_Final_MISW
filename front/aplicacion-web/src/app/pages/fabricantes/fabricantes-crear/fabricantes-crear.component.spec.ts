import { TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of } from 'rxjs';
import { FabricantesCrearComponent } from './fabricantes-crear.component';
import { FabricantesCrearService } from './fabricantes-crear.service';

describe('FabricantesCrearComponent', () => {
  let serviceSpy: jasmine.SpyObj<FabricantesCrearService>;

  beforeEach(async () => {
    serviceSpy = jasmine.createSpyObj('FabricantesCrearService', ['crearFabricante']);

    await TestBed.configureTestingModule({
      imports: [
        FabricantesCrearComponent,
        ReactiveFormsModule,
        HttpClientTestingModule
      ],
      providers: [{ provide: FabricantesCrearService, useValue: serviceSpy }]
    }).compileComponents();
  });

  it('should create', () => {
    const fixture = TestBed.createComponent(FabricantesCrearComponent);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('should have invalid form when empty', () => {
    const fixture = TestBed.createComponent(FabricantesCrearComponent);
    const comp = fixture.componentInstance;
    comp.ngOnInit(); 
    expect(comp.fabricanteForm.valid).toBeFalse();
  });
  
  it('should call service on valid submit', () => {
    const fixture = TestBed.createComponent(FabricantesCrearComponent);
    const comp = fixture.componentInstance;
    comp.ngOnInit(); 
  
    serviceSpy.crearFabricante.and.returnValue(of());
  
    comp.fabricanteForm.setValue({
      nombre: 'Prueba',
      correo: 'prueba@correo.com',
      telefono: '1234567',
      empresa: 'Empresa Prueba'
    });
  
    comp.onSubmit();
    expect(serviceSpy.crearFabricante).toHaveBeenCalledWith(jasmine.objectContaining({ nombre: 'Prueba' }));
  });
});