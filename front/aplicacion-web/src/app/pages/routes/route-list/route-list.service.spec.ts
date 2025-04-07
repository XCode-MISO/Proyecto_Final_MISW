import { TestBed } from '@angular/core/testing';

import { RouteListService } from './route-list.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideNativeDateAdapter } from '@angular/material/core';

describe('RouteListService', () => {
  let service: RouteListService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        provideNativeDateAdapter()
      ]
    });
    service = TestBed.inject(RouteListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
