import { Component } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpContext, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { FormGroup, FormControl, Validators, ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  constructor(private http: HttpClient) { }

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
    firstName: new FormControl('Test'),
    lastName: new FormControl('Test'),
    email: new FormControl('test@test.com', [Validators.required, Validators.email]),
    password: new FormControl('test123', [Validators.required, Validators.minLength(6)]),
    confirmPassword: new FormControl('test123', Validators.required),
    zipCode: new FormControl('61554', [Validators.required, Validators.pattern(/^\d{5}(-\d{4})?$/)]),
  }, { validators: this.checkPasswords });

  signIn(): void {
  }

  signUp(): void {
    const endpoint: string = environment.apiUrl + "/signup";
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

  swapForm(id: string): void {
    this.hideAllForms();
    this.showForm(id);
  }

  ngOnInit(): void {
    this.hideAllForms();
    this.showForm('signup-form');
  }
}
