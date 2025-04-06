import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FabricantesListarComponent } from './fabricantes-listar.component';

describe('FabricantesListarComponent', () => {
  let component: FabricantesListarComponent;
  let fixture: ComponentFixture<FabricantesListarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FabricantesListarComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FabricantesListarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
