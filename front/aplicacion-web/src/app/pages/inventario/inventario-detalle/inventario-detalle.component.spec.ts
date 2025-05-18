import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalleProductoComponent } from './inventario-detalle.component';
import { ActivatedRoute } from '@angular/router';
import { of, throwError } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { CommonModule } from '@angular/common';
import { InventarioListService, DetalleInventarioProducto } from '../inventario-listar/inventario-list.service';

describe('DetalleProductoComponent', () => {
  let component: DetalleProductoComponent;
  let fixture: ComponentFixture<DetalleProductoComponent>;
  let mockInventarioService: jasmine.SpyObj<InventarioListService>;

  const mockProducto: DetalleInventarioProducto = {
    producto_id: 1,
    nombre: 'Producto de prueba',
    bodega: 'Bodega Central',
    pasillo: 'A1',
    estante: 'E3',
    stock: 50,
    precio: 100,
    moneda: 'USD',
  };

  beforeEach(async () => {
    mockInventarioService = jasmine.createSpyObj('InventarioListService', ['getInventarioId']);

    await TestBed.configureTestingModule({
      imports: [
        CommonModule,
        FormsModule,
        TranslateModule.forRoot(),
        DetalleProductoComponent, // ✅ importar componente standalone
      ],
      providers: [
        { provide: InventarioListService, useValue: mockInventarioService },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: {
                get: () => '1' // ID válido por defecto
              }
            }
          }
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(DetalleProductoComponent);
    component = fixture.componentInstance;
  });

  it('debería crear el componente', () => {
    expect(component).toBeTruthy();
  });

  it('debería cargar el producto con ID válido y calcular precio en USD', () => {
    mockInventarioService.getInventarioId.and.returnValue(of(mockProducto));

    component.ngOnInit();

    expect(mockInventarioService.getInventarioId).toHaveBeenCalledWith(1);
    expect(component.producto).toEqual(mockProducto);
    expect(component.precioConvertido).toEqual(100); // Precio sin conversión
  });

  it('debería calcular el precio en COP si se selecciona COP', () => {
    mockInventarioService.getInventarioId.and.returnValue(of(mockProducto));

    component.ngOnInit();
    component.monedaSeleccionada = 'COP';
    component.actualizarPrecio();

    expect(component.precioConvertido).toEqual(100 * component['tasaCambioUSD']);
  });

  it('debería mostrar error si el ID no es un número', async () => {
    await TestBed.resetTestingModule().configureTestingModule({
        imports: [
        CommonModule,
        FormsModule,
        TranslateModule.forRoot(),
        DetalleProductoComponent,
        ],
        providers: [
        { provide: InventarioListService, useValue: mockInventarioService },
        {
            provide: ActivatedRoute,
            useValue: {
            snapshot: {
                paramMap: {
                get: () => 'abc', // ID inválido
                }
            }
            }
        }
        ]
    }).compileComponents();

    const invalidFixture = TestBed.createComponent(DetalleProductoComponent);
    const invalidComponent = invalidFixture.componentInstance;
    invalidComponent.ngOnInit();

    expect(invalidComponent.error).toBe('ID inválido');
    expect(invalidComponent.producto).toBeNull();
  });

  it('debería manejar error si el servicio falla', () => {
    mockInventarioService.getInventarioId.and.returnValue(throwError(() => new Error('Error de servicio')));

    component.ngOnInit();

    expect(component.error).toBe('Error al cargar el detalle del producto');
    expect(component.producto).toBeNull();
  });
});
