import { TestBed } from '@angular/core/testing';

import { RouteListService } from './route-list.service';

describe('RouteListService', () => {
  let service: RouteListService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RouteListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
