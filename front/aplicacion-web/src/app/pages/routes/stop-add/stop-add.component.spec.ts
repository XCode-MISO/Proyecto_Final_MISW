import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StopAddComponent } from './stop-add.component';

describe('StopAddComponent', () => {
  let component: StopAddComponent;
  let fixture: ComponentFixture<StopAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StopAddComponent]
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
