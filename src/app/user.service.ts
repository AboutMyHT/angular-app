import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { Observable, firstValueFrom } from 'rxjs';
import { map } from 'rxjs/operators';

import { User } from './user'

@Injectable({
  providedIn: 'root'
})
export class UserService {
  currentUser: User | null = null;

  constructor(private http: HttpClient) {
  }

  getToken(): string | null {
    return localStorage.getItem('sessionToken');
  }

  isLoggedIn(): boolean {
    return localStorage.getItem('sessionToken') !== null;
  }

  initializeUser(): Promise<User | null> {
    return new Promise((resolve, reject) => {
      if (this.isLoggedIn()) {
        const endpoint: string = environment.apiUrl + "/session";
        this.http.post<{ user: User }>(endpoint, {
          session_token: localStorage.getItem('sessionToken')
        }).pipe(
          map(response => response.user)
        ).subscribe({
          error: (error) => {
            console.error("Failed to fetch current user", error);
            localStorage.removeItem('sessionToken');
            window.location.reload();
            resolve(null);
          },
          next: (user) => {
            this.currentUser = User.fromObject(user);
            resolve(user);
          }
        });
      } else {
        resolve(null);
      }
    })
  }

  async updateUser(
    sessionToken: string,
    zipCode: string,
    firstName: string = "",
    lastName: string = "",
    bioInfo: string = "",
    successCallback: Function = () => { },
    failureCallback: Function = () => { },
  ): Promise<boolean> {
    const endpoint: string = environment.apiUrl + "/updateuser";

    try {
      const user = await firstValueFrom(this.http.post<{ user: User }>(endpoint, {
        session_token: sessionToken,
        zip_code: zipCode,
        first_name: firstName,
        last_name: lastName,
        bio_info: bioInfo,
      }).pipe(
        map(response => response.user)
      ));

      successCallback(user);

      return true;
    } catch (error) {
      failureCallback(error);
      return false;
    }
  }

  async signupUser(
    email: string,
    zipCode: string,
    password: string,
    firstName: string = "",
    lastName: string = "",
    emailVerified: boolean = false,
    needsPasswordReset: boolean = false,
    successCallback: Function = () => { },
    failureCallback: Function = () => { },
  ): Promise<boolean> {
    const endpoint: string = environment.apiUrl + "/signup";

    try {
      const user = await firstValueFrom(this.http.post<{ user: User }>(endpoint, {
        email: email,
        zip_code: zipCode,
        password: password,
        first_name: firstName,
        last_name: lastName,
        email_verified: emailVerified,
        needs_password_reset: needsPasswordReset
      }).pipe(
        map(response => response.user)
      ));

      successCallback(user);

      return true;
    } catch (error) {
      failureCallback(error);
      return false;
    }
  }

  async signinUser(
    email: string,
    password: string,
    successCallback: Function = () => { },
    failureCallback: Function = () => { },
  ): Promise<boolean> {
    const endpoint: string = environment.apiUrl + "/signin";

    try {
      const response = await firstValueFrom(this.http.post<{ user: User, session_token: string }>(endpoint, {
        email: email,
        password: password,
      }));

      const user = response.user;
      const sessionToken = response.session_token;

      localStorage.setItem('sessionToken', sessionToken);

      successCallback(user);

      return true;
    } catch (error) {
      failureCallback(error);
      return false;
    }
  }
}
