import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendedorAddComponent } from './vendedor-add.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { AuthModule } from '@angular/fire/auth';

xdescribe('VendedorAddComponent', () => {
  let component: VendedorAddComponent;
  let fixture: ComponentFixture<VendedorAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        VendedorAddComponent, 
        HttpClientTestingModule,
        AuthModule
      ]
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
