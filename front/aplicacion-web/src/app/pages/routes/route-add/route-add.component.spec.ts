import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RouteAddComponent } from './route-add.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideNativeDateAdapter } from '@angular/material/core';

describe('RouteAddComponent', () => {
  let component: RouteAddComponent;
  let fixture: ComponentFixture<RouteAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouteAddComponent, HttpClientTestingModule, RouterTestingModule],
      providers: [
        provideNativeDateAdapter()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RouteAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
