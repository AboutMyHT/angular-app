import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { User } from './user'

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) { }

  signupUser(
    email: string,
    zipCode: string,
    password: string,
    firstName: string = "",
    lastName: string = "",
    emailVerified: boolean = false,
    needsPasswordReset: boolean = false,
  ): Observable<User> {
    const endpoint: string = environment.apiUrl + "/signup";

    return this.http.post<{ user: User }>(endpoint, {
      email: email,
      zip_code: zipCode,
      password: password,
      first_name: firstName,
      last_name: lastName,
      email_verified: emailVerified,
      needs_password_reset: needsPasswordReset
    }).pipe(
      map(response => response.user)
    );
  }

  signinUser(
    email: string,
    password: string
  ): Observable<User> {
    const endpoint: string = environment.apiUrl + "/signin";

    return this.http.post<{ user: User }>(endpoint, {
      email: email,
      password: password,
    }).pipe(
      map(response => response.user)
    );
  }
}
