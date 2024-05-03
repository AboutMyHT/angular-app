/*
  Purpose: This guard is used to protect routes that require the user to be UNauthenticated.
  Requirements: 4.3.1; 4.4.1
*/
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

import { UserService } from './user.service';

export const guestGuard: CanActivateFn = (route, state) => {
  return !inject(UserService).isLoggedIn()
    ? true
    : inject(Router).createUrlTree(['/home']);
};
