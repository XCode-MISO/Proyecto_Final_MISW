import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { GestionFabricantesComponent } from './gestion-fabricantes.component';

describe('GestionFabricantesComponent', () => {
  let component: GestionFabricantesComponent;
  let fixture: ComponentFixture<GestionFabricantesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        GestionFabricantesComponent, 
        RouterTestingModule  
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GestionFabricantesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});