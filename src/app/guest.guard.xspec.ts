import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { guestGuard } from './guest.guard';

xdescribe('guestGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.inject(guestGuard).canActivate(...guardParameters);

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
