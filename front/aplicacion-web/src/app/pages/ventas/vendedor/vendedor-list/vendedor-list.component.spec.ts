import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendedorListComponent } from './vendedor-list.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideNativeDateAdapter } from '@angular/material/core';
import { TranslateModule } from '@ngx-translate/core';

describe('VendedorListComponent', () => {
  let component: VendedorListComponent;
  let fixture: ComponentFixture<VendedorListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        VendedorListComponent, 
        HttpClientTestingModule,
        TranslateModule.forRoot()
      ],
      providers: [
        provideNativeDateAdapter()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VendedorListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});