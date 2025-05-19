import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideNativeDateAdapter } from '@angular/material/core';
import { TranslateModule } from '@ngx-translate/core';
import { MatTableModule } from '@angular/material/table';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { NO_ERRORS_SCHEMA } from '@angular/core';

import { VendedorReportesComponent } from './vendedor-reportes.component';

fdescribe('VendedorReportesComponent', () => {
  let component: VendedorReportesComponent;
  let fixture: ComponentFixture<VendedorReportesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        VendedorReportesComponent,
        HttpClientTestingModule,
        TranslateModule.forRoot(),
        MatTableModule
      ],
      providers: [
        provideNativeDateAdapter(),
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: {
                get: () => '123'
              }
            }
          }
        }
      ],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VendedorReportesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});