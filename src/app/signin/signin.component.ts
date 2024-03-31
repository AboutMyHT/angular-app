
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn, AbstractControl, ValidationErrors, FormGroupName } from '@angular/forms';

import { User } from '../user';

import { UserService } from '../user.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})

export class SigninComponent {
  isLoggedIn: boolean;
  constructor(private userService: UserService, private router: Router) {
    this.isLoggedIn = this.userService.isLoggedIn();
  }

  alertMessage: string = '';
  alertType: string = '';
  alertPreferForm: string = '';
  alertPreferText: string = '';

  checkPasswords: ValidatorFn = (group: AbstractControl): ValidationErrors | null => {
    let pass = group.get('password')?.value;
    let confirmPass = group.get('confirmPassword')?.value
    return pass === confirmPass ? null : { noMatch: true }
  }

  signInForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)]),
  });

  signUpForm = new FormGroup({
    firstName: new FormControl(''),
    lastName: new FormControl(''),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)]),
    confirmPassword: new FormControl('', Validators.required),
    zipCode: new FormControl('', [Validators.required, Validators.pattern(/^\d{5}(-\d{4})?$/)]),
  }, { validators: this.checkPasswords });

  signIn(): void {
    if (!this.signInForm.invalid) {
      this.userService.signinUser(
        this.signInForm.get('email')?.value!,
        this.signInForm.get('password')?.value!,
        (userData: User) => { // Success callback
          this.router.navigate(['/']);
          window.location.reload();
        },
        (error: HttpErrorResponse) => { // Failure callback
          if (error.error == "Invalid email or password") {
            this.showAlert("Invalid email or password! Please try again.", "danger");
          } else {
            this.showAlert(error.error, "danger");
          }
        }
      );
    }
  }

  signUp(): void {
    if (!this.signUpForm.invalid) {
      this.userService.signupUser(
        this.signUpForm.get('email')?.value!,
        this.signUpForm.get('zipCode')?.value!,
        this.signUpForm.get('password')?.value!,
        this.signUpForm.get('firstName')?.value || '',
        this.signUpForm.get('lastName')?.value || '',
        false, false,
        () => {// Success callback
          this.resetForms();
          this.showAlert("Account created successfully! Please sign in.", "success");
          this.swapForm('signin-form');
        },
        (error: HttpErrorResponse) => {// Failure callback
          if (error.error == "User exists") {
            this.showAlert("That email address is already in use.", "danger", "signin-form", "Sign in instead.");
          } else {
            this.showAlert(error.error, "danger");
          }
        },
      );
    }
  }

  hideAllForms(): void {
    const formGroups = document.getElementsByClassName('form-group');
    for (let i = 0; i < formGroups.length; i++) {
      const formGroup = formGroups[i] as HTMLElement;
      formGroup.style.display = 'none';
    }
  }

  showForm(id: string): void {
    const formGroup = document.getElementById(id);
    if (formGroup) {
      formGroup.style.display = 'block';
    }
  }

  resetForms(): void {
    this.signInForm.reset();
    this.signUpForm.reset();
  }

  swapForm(id: string): void {
    this.hideAllForms();
    this.showForm(id);
  }

  showAlert(message: string, type: string = "danger", preferedForm: string = "", preferedText: string = ""): void {
    this.alertMessage = message;
    this.alertType = type;
    this.alertPreferForm = preferedForm;
    this.alertPreferText = preferedText;
  }

  dismissAlert(): void {
    this.alertMessage = '';
    this.alertType = '';
    this.alertPreferForm = '';
    this.alertPreferText = '';
  }

  ngOnInit(): void {
    this.hideAllForms();
    this.showForm('signin-form');
  }
}
