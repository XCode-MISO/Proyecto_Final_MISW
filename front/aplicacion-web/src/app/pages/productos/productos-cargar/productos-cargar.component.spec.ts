import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { of } from 'rxjs';
import { ProductosCargarComponent } from './productos-cargar.component';
import { ProductosService } from './productos.service';
import { HttpClientModule } from '@angular/common/http';

const mockFabricantes = [
  { id: 1, nombre: 'Fab A' },
  { id: 2, nombre: 'Fab B' }
];

describe('ProductosCargarComponent', () => {
  let serviceSpy: jasmine.SpyObj<ProductosService>;

  beforeEach(async () => {
    serviceSpy = jasmine.createSpyObj('ProductosService', ['obtenerFabricantes', 'cargarProducto']);
    serviceSpy.obtenerFabricantes.and.returnValue(of(mockFabricantes));
    serviceSpy.cargarProducto.and.returnValue(of());

    await TestBed.configureTestingModule({
      imports: [ProductosCargarComponent, ReactiveFormsModule, HttpClientTestingModule],
      providers: [{ provide: ProductosService, useValue: serviceSpy }]
    }).compileComponents();
  });

  it('should create', () => {
    const fixture = TestBed.createComponent(ProductosCargarComponent);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('form invalid when empty', () => {
    const comp = TestBed.createComponent(ProductosCargarComponent).componentInstance;
    comp.ngOnInit();
    expect(comp.form.valid).toBeFalse();
  });

  it('should call service on valid submit', () => {
    const fixture = TestBed.createComponent(ProductosCargarComponent);
    const comp = fixture.componentInstance;
    comp.ngOnInit();

    comp.form.setValue({ nombre: 'Prod', fabricanteId: 1, cantidad: 10, precio: 5.5, moneda: 'USD', bodega: 'Bodega 1', estante: 'Estante 1', pasillo: 'Pasillo 1' });
    comp.onSubmit();

    expect(serviceSpy.cargarProducto).toHaveBeenCalledWith(jasmine.objectContaining({ nombre: 'Prod' }));
  });
});

xdescribe('ProductosCargarComponent – validaciones', () => {
    let comp: ProductosCargarComponent;
  
    beforeEach(async () => {
      await TestBed.configureTestingModule({
        imports: [ProductosCargarComponent, ReactiveFormsModule, HttpClientModule],
        providers: [ProductosService]
      }).compileComponents();
  
      comp = TestBed.createComponent(ProductosCargarComponent).componentInstance;
      comp.ngOnInit();
    });
  
    it('form vacío es inválido', () => {
      expect(comp.form.valid).toBeFalse();
    });
  
    it('cantidad negativa es inválida', () => {
      comp.form.patchValue({ nombre: 'P', fabricanteId: 8, cantidad: -1, precio: 10, moneda: 'COP', bodega: 'Bodega 1', estante: 'Estante 1', pasillo: 'Pasillo 1' });
      expect(comp.f['cantidad'].valid).toBeFalse();
    });
  
    it('precio cero es inválido', () => {
      comp.form.patchValue({ nombre: 'P', fabricanteId: 8, cantidad: 1, precio: 0, moneda: 'COP', bodega: 'Bodega 1', estante: 'Estante 1', pasillo: 'Pasillo 1' });
      expect(comp.f['precio'].valid).toBeFalse();
    });
  });