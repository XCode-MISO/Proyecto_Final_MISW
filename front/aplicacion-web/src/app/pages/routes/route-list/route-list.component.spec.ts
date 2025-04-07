import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RouteListComponent } from './route-list.component';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideNativeDateAdapter } from '@angular/material/core';
import { RouterTestingModule } from '@angular/router/testing';

describe('RouteListComponent', () => {
  let component: RouteListComponent;
  let fixture: ComponentFixture<RouteListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouteListComponent, HttpClientTestingModule, RouterTestingModule],
      providers: [
        provideNativeDateAdapter()
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(RouteListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
