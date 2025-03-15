import { TestBed } from '@angular/core/testing';

import { StainService } from './stain.service';

describe('StainService', () => {
  let service: StainService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StainService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
