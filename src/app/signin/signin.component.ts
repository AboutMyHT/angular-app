
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn, AbstractControl, ValidationErrors, FormGroupName } from '@angular/forms';

import { User } from '../user';

import { UserService } from '../user.service';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})

export class SigninComponent {
  constructor(private userService: UserService, private router: Router) { }

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
    email: new FormControl('default@def.ault', [Validators.required, Validators.email]),
    password: new FormControl('default', [Validators.required, Validators.minLength(6)]),
  });

  signUpForm = new FormGroup({
    firstName: new FormControl('default'),
    lastName: new FormControl('default'),
    email: new FormControl('default@def.ault', [Validators.required, Validators.email]),
    password: new FormControl('default', [Validators.required, Validators.minLength(6)]),
    confirmPassword: new FormControl('default', Validators.required),
    zipCode: new FormControl('61554', [Validators.required, Validators.pattern(/^\d{5}(-\d{4})?$/)]),
  }, { validators: this.checkPasswords });

  signIn(): void {
    if (!this.signInForm.invalid) {
      this.userService.signinUser(
        this.signInForm.get('email')?.value!,
        this.signInForm.get('password')?.value!
      ).subscribe(
        {
          error: (error) => {
            if (error.error == "Invalid email or password") {
              this.showAlert("Invalid email or password! Please try again.", "danger");
            } else {
              this.showAlert(error.error, "danger");
            }
          },
          next: (userData) => {
            const user = User.fromObject(userData);
            this.showAlert("Succesful login for '" + user.toString() + "', however logging in is not implemented yet.", "success");
            this.resetForms();
          },
          complete: () => {
            this.swapForm('signin-form');
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
      ).subscribe(
        {
          error: (error) => {
            if (error.error == "User exists") {
              this.showAlert("That email address is already in use.", "danger", "signin-form", "Sign in instead.");
            } else {
              this.showAlert(error.error, "danger");
            }
          },
          next: (user) => {
            this.resetForms();
          },
          complete: () => {
            this.showAlert("Account created successfully! Please sign in.", "success");
            this.swapForm('signin-form');
          }
        }
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
