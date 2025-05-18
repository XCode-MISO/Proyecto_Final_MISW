import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ProductoComponent } from './producto.component';
import { Router } from '@angular/router';
import { of } from 'rxjs';
import { InventarioListService, Inventario } from './inventario-listar/inventario-list.service';
import { TranslateModule } from '@ngx-translate/core';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';

// Mock de productos
const MOCK_PRODUCTOS: Inventario[] = [
  { producto_id: 1, nombre: 'Producto A', bodega: 'Bodega A', cantidad: 10 },
  { producto_id: 2, nombre: 'Producto B', bodega: 'Bodega B', cantidad: 5 },
  { producto_id: 3, nombre: 'Zapato', bodega: 'Central', cantidad: 15 },
];

describe('ProductoComponent', () => {
  let component: ProductoComponent;
  let fixture: ComponentFixture<ProductoComponent>;
  let mockInventarioService: jasmine.SpyObj<InventarioListService>;
  let mockRouter: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    mockInventarioService = jasmine.createSpyObj('InventarioListService', ['getInventario']);
    mockRouter = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [ProductoComponent, CommonModule, FormsModule, MatIconModule, TranslateModule.forRoot()],
      providers: [
        { provide: InventarioListService, useValue: mockInventarioService },
        { provide: Router, useValue: mockRouter },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ProductoComponent);
    component = fixture.componentInstance;
  });

  it('debería crear el componente', () => {
    expect(component).toBeTruthy();
  });

  it('debería cargar productos al inicializar y filtrar correctamente', () => {
    mockInventarioService.getInventario.and.returnValue(of(MOCK_PRODUCTOS));

    fixture.detectChanges(); // ejecuta ngOnInit

    expect(component.productosOriginales.length).toBe(3);
    expect(component.productosFiltrados.length).toBe(3);

    component.filtroNombre = 'zap';
    component.actualizarFiltro();

    expect(component.productosFiltrados.length).toBe(1);
    expect(component.productosFiltrados[0].nombre).toContain('Zapato');
  });

  it('debería navegar al detalle del producto', () => {
    component.navigateToDetalle(42);
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/inventario/detalle/', 42]);
  });

  it('debería usar trackByProductoId correctamente', () => {
    const productoMock = { producto_id: 99, nombre: 'X', bodega: 'Y', cantidad: 1 };
    expect(component.trackByProductoId(0, productoMock)).toBe(99);
  });
});
