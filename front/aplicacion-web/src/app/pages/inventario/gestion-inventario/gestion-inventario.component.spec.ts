
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { GestionInventarioComponent } from './gestion-inventario.component';

describe('GestionFabricantesComponent', () => {
  let component: GestionInventarioComponent;
  let fixture: ComponentFixture<GestionInventarioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        GestionInventarioComponent, 
        RouterTestingModule  
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GestionInventarioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});