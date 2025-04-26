import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ProductosUploadComponent } from './productos-upload.component';
import { ProductosUploadService } from './productos-upload.service';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

describe('ProductosUploadComponent', () => {
  let component: ProductosUploadComponent;
  let fixture: ComponentFixture<ProductosUploadComponent>;
  let uploadServiceSpy: jasmine.SpyObj<ProductosUploadService>;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    const spyService = jasmine.createSpyObj('ProductosUploadService', ['uploadFile']);
    const spyRouter = jasmine.createSpyObj('Router', ['navigate']);


    await TestBed.configureTestingModule({
      imports: [
        ProductosUploadComponent,    
        CommonModule,                 
        ReactiveFormsModule
      ],
      providers: [
        { provide: ProductosUploadService, useValue: spyService },
        { provide: Router, useValue: spyRouter }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ProductosUploadComponent);
    component = fixture.componentInstance;
    uploadServiceSpy = TestBed.inject(ProductosUploadService) as jasmine.SpyObj<ProductosUploadService>;
    routerSpy = TestBed.inject(Router) as jasmine.SpyObj<Router>;
    fixture.detectChanges();
  });

  it('debería crear el componente', () => {
    expect(component).toBeTruthy();
  });

  it('debería asignar mensaje de error si no se selecciona archivo', () => {
    component.selectedFile = null;
    component.uploadFile();
    expect(component.message).toEqual('No hay archivo seleccionado.');
  });

  it('debería llamar al servicio uploadFile y establecer mensaje en caso de éxito', () => {
    const fakeResponse = { inserted: 2, errors: [] };
    uploadServiceSpy.uploadFile.and.returnValue(of(fakeResponse));
    const dummyFile = new File(["data"], "Productos.csv", { type: "text/csv" });
    component.selectedFile = dummyFile;
    component.uploadFile();
    expect(uploadServiceSpy.uploadFile).toHaveBeenCalled();
    expect(component.message).toContain('Carga exitosa');
    expect(component.isLoading).toBeFalse();
  });

  it('debería gestionar error en la carga', () => {
    uploadServiceSpy.uploadFile.and.returnValue(throwError(() => new Error("Error al subir")));
    const dummyFile = new File(["data"], "Productos.csv", { type: "text/csv" });
    component.selectedFile = dummyFile;
    component.uploadFile();
    expect(component.isLoading).toBeFalse();
    expect(component.message).toEqual('Error al cargar el archivo.');
  });

  it('el botón cancelar debe limpiar el formulario y navegar a "/productos/seleccion-carga-producto"', () => {
    component.selectedFile = new File(["dummy"], "dummy.csv");
    component.message = "Mensaje previo";
    component.errorMessages = ["Error 1"];
    component.isLoading = true;
    component.cancelar();

    expect(component.selectedFile).toBeNull();
    expect(component.message).toEqual('');
    expect(component.errorMessages).toEqual([]);
    expect(component.isLoading).toBeFalse();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/productos/seleccion-carga']);
  });
});