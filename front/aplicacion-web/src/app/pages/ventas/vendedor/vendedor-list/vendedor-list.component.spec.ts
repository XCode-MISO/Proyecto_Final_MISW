import { ComponentFixture, TestBed } from '@angular/core/testing';
import { VendedorListComponent } from './vendedor-list.component';
import { VendedorService } from '../vendedor.service';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';

fdescribe('VendedorListComponent', () => {
  let component: VendedorListComponent;
  let fixture: ComponentFixture<VendedorListComponent>;
  let vendedorService: jasmine.SpyObj<VendedorService>;
  let router: jasmine.SpyObj<Router>;

  // Datos mock para pruebas
  const mockVendedores = [
    { 
      id: '1', 
      nombre: 'María Fernanda González López',
      correo: 'mariaf@example.com',
      telefono: '3101234567',
      direccion: 'Calle 123 #45-67',
      imagen: 'https://example.com/imagen1.jpg'
    },
    { 
      id: '2', 
      nombre: 'Juan Carlos Rodríguez',
      correo: 'juanc@example.com',
      telefono: '3109876543',
      direccion: 'Carrera 78 #90-12',
      imagen: 'https://example.com/imagen2.jpg'
    }
  ];

  beforeEach(async () => {
    // Crear spies para los servicios
    const vendedorServiceSpy = jasmine.createSpyObj('VendedorService', ['getVendedores']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        CommonModule,
        MatButtonModule,
        VendedorListComponent // IMPORTANTE: Importarlo aquí en vez de declararlo
      ],
      providers: [
        { provide: VendedorService, useValue: vendedorServiceSpy },
        { provide: Router, useValue: routerSpy }
      ],
      schemas: [NO_ERRORS_SCHEMA] // Para ignorar errores de elementos no reconocidos como mat-button
    }).compileComponents();

    vendedorService = TestBed.inject(VendedorService) as jasmine.SpyObj<VendedorService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VendedorListComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    vendedorService.getVendedores.and.returnValue(of([]));
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should load vendedores on init', () => {
    // Configurar el comportamiento del spy
    vendedorService.getVendedores.and.returnValue(of(mockVendedores));
    
    // Inicializar componente
    fixture.detectChanges();
    
    // Verificar que se llamó al servicio
    expect(vendedorService.getVendedores).toHaveBeenCalled();
    
    // Verificar que los datos se cargaron correctamente
    expect(component.vendedores.length).toBe(2);
    expect(component.vendedores[0].nombre).toBe('María Fernanda González López');
  });

  it('should handle error when loading vendedores', () => {
    // Espiar console.error
    spyOn(console, 'error');
    
    // Configurar el spy para lanzar error
    vendedorService.getVendedores.and.returnValue(throwError(() => new Error('Error al cargar')));
    
    // Inicializar componente
    fixture.detectChanges();
    
    // Verificar que se registró el error
    expect(console.error).toHaveBeenCalled();
    
    // Verificar que vendedores está vacío
    expect(component.vendedores.length).toBe(0);
  });

  it('should navigate to informes page when verInformes is called', () => {
    const vendedorId = '1';
    component.verInformes(vendedorId);
    expect(router.navigate).toHaveBeenCalledWith(['/ventas/vendedor/informes', vendedorId]);
  });

  it('should navigate to reportes page when verReportes is called', () => {
    const vendedorId = '1';
    component.verReportes(vendedorId);
    expect(router.navigate).toHaveBeenCalledWith(['/ventas/vendedor/reportes', vendedorId]);
  });

  it('should display "No hay vendedores registrados" when vendedores array is empty', () => {
    // Configurar el comportamiento del spy
    vendedorService.getVendedores.and.returnValue(of([]));
    
    // Inicializar componente
    fixture.detectChanges();
    
    // Obtener el elemento del DOM
    const compiled = fixture.nativeElement;
    expect(compiled.textContent).toContain('No hay vendedores registrados');
  });

  it('should display vendedor cards when vendedores array is not empty', () => {
    // Configurar el comportamiento del spy
    vendedorService.getVendedores.and.returnValue(of(mockVendedores));
    
    // Inicializar componente
    fixture.detectChanges();
    
    // Obtener elementos del DOM
    const compiled = fixture.nativeElement;
    const vendedorCards = compiled.querySelectorAll('.vendedor-card');
    
    // Verificar que se muestran dos tarjetas de vendedor
    expect(vendedorCards.length).toBe(2);
    
    // Verificar que se muestra el nombre del vendedor
    expect(compiled.textContent).toContain('María Fernanda González López');
    expect(compiled.textContent).toContain('Juan Carlos Rodríguez');
  });
});
