import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendedorAddComponent } from './vendedor-add.component';

describe('VendedorAddComponent', () => {
  let component: VendedorAddComponent;
  let fixture: ComponentFixture<VendedorAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VendedorAddComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VendedorAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
