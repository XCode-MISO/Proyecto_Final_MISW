import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StopAddComponent } from './stop-add.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideNativeDateAdapter } from '@angular/material/core';

describe('StopAddComponent', () => {
  let component: StopAddComponent;
  let fixture: ComponentFixture<StopAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StopAddComponent, HttpClientTestingModule, RouterTestingModule],
      providers: [
        provideNativeDateAdapter()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StopAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
