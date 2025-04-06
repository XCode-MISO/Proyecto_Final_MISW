import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionFabricantesComponent } from './gestion-fabricantes.component';

describe('GestionFabricantesComponent', () => {
  let component: GestionFabricantesComponent;
  let fixture: ComponentFixture<GestionFabricantesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GestionFabricantesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestionFabricantesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
