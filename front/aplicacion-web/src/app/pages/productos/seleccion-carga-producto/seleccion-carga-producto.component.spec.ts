import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { SeleccionCargaProductoComponent } from './seleccion-carga-producto.component';
import { By } from '@angular/platform-browser';

describe('SeleccionCargaProductoComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SeleccionCargaProductoComponent, RouterTestingModule],
    }).compileComponents();
  });

  it('should create the component', () => {
    const fixture = TestBed.createComponent(SeleccionCargaProductoComponent);
    const component = fixture.componentInstance;
    expect(component).toBeTruthy();
  });

  it('should display the heading "Carga Productos"', () => {
    const fixture = TestBed.createComponent(SeleccionCargaProductoComponent);
    fixture.detectChanges(); 
    const headingEl = fixture.debugElement.query(By.css('h2'));
    expect(headingEl.nativeElement.textContent).toContain('Carga Productos');
  });

  it('should display two buttons with the proper texts', () => {
    const fixture = TestBed.createComponent(SeleccionCargaProductoComponent);
    fixture.detectChanges();
    const buttons = fixture.debugElement.queryAll(By.css('.btn-carga'));
    expect(buttons.length).toBe(2);
    const buttonTexts = buttons.map(btn => btn.nativeElement.textContent.trim());
    expect(buttonTexts).toEqual(['Carga Individual', 'Carga Masiva']);
  });

  it('should navigate to "/productos/crear" when the "Carga Individual" button is clicked', () => {
    const fixture = TestBed.createComponent(SeleccionCargaProductoComponent);
    const component = fixture.componentInstance;
    const router = TestBed.inject(RouterTestingModule);
    spyOn(component, 'irCargaIndividual');
    const individualButton = fixture.debugElement.queryAll(By.css('.btn-carga'))[0];
    individualButton.triggerEventHandler('click', null);
    expect(component.irCargaIndividual).toHaveBeenCalled();
  });

  it('should navigate to "/productos/upload" when the "Carga Masiva" button is clicked', () => {
    const fixture = TestBed.createComponent(SeleccionCargaProductoComponent);
    const component = fixture.componentInstance;
    spyOn(component, 'irCargaMasiva');
    const masivaButton = fixture.debugElement.queryAll(By.css('.btn-carga'))[1];
    masivaButton.triggerEventHandler('click', null);
    expect(component.irCargaMasiva).toHaveBeenCalled();
  });
});