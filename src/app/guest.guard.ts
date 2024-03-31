

import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

import { UserService } from './user.service';

export const guestGuard: CanActivateFn = (route, state) => {
  return !inject(UserService).isLoggedIn()
    ? true
    : inject(Router).createUrlTree(['/home']);
};
