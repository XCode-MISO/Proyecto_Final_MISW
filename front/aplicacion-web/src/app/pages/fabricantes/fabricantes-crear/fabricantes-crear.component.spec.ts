import { TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of } from 'rxjs';
import { FabricantesCrearComponent } from './fabricantes-crear.component';
import { FabricantesCrearService } from './fabricantes-crear.service';
import { HttpClientModule } from '@angular/common/http';

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


describe('FabricantesCrearComponent – validación de formulario', () => {
    let comp: FabricantesCrearComponent;
  
    beforeEach(async () => {
      await TestBed.configureTestingModule({
        imports: [FabricantesCrearComponent, ReactiveFormsModule, HttpClientModule],
        providers: [FabricantesCrearService]
      }).compileComponents();
  
      comp = TestBed.createComponent(FabricantesCrearComponent).componentInstance;
      comp.ngOnInit();
    });
  
    it('debe ser inválido con campos vacíos', () => {
      expect(comp.fabricanteForm.valid).toBeFalse();
    });
  
    it('correo inválido no pasa la validación', () => {
      comp.fabricanteForm.patchValue({
        nombre: 'A', correo: 'invalido', telefono: '1234567', empresa: 'E' });
      expect(comp.f['correo'].valid).toBeFalse();
      expect(comp.fabricanteForm.valid).toBeFalse();
    });
  
    it('teléfono fuera de rango no es válido', () => {
      comp.fabricanteForm.patchValue({
        nombre: 'A', correo: 'a@a.com', telefono: '12', empresa: 'E' });
      expect(comp.f['telefono'].valid).toBeFalse();
    });
  });