import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RouteAddComponent } from './route-add.component';

describe('RouteAddComponent', () => {
  let component: RouteAddComponent;
  let fixture: ComponentFixture<RouteAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouteAddComponent]
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
