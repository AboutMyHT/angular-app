/*
  Purpose: This guard is used to protect routes that require the user to be authenticated.
  Requirements: 4.1.1; 4.5.1; 4.6.1
*/
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

import { UserService } from './user.service';

export const authGuard: CanActivateFn = (route, state) => {
  return inject(UserService).isLoggedIn()
    ? true
    : inject(Router).createUrlTree(['/signin']);
};
