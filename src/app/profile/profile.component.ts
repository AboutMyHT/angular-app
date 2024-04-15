import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';

import { User } from '../user';

import { UserService } from '../user.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  currentUser: User;
  updateUserForm: FormGroup;

  constructor(private userService: UserService, private router: Router) {
    this.currentUser = this.userService.currentUser!;

    this.updateUserForm = new FormGroup({
      firstName: new FormControl(this.currentUser.firstName),
      lastName: new FormControl(this.currentUser.lastName),
      email: new FormControl(this.currentUser.email, [Validators.required, Validators.email]),
      zipCode: new FormControl(this.currentUser.zipCode, [Validators.required, Validators.pattern(/^\d{5}(-\d{4})?$/)]),
    })
  }

  isLoading: boolean = false;

  alertMessage: string = '';
  alertType: string = '';
  alertPreferForm: string = '';
  alertPreferText: string = '';

  updateUser(): void {
    if (!this.updateUserForm.invalid) {
      this.startLoading();

      this.userService.updateUser(
        this.userService.getToken()!,
        this.updateUserForm.get('zipCode')?.value!,
        this.updateUserForm.get('firstName')?.value!,
        this.updateUserForm.get('lastName')?.value!,
        (userData: User) => { // Success callback
          this.stopLoading();
          window.location.reload();
        },
        (error: HttpErrorResponse) => { // Failure callback
          this.stopLoading();
          this.showAlert(error.error, "danger");
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
    this.isLoading = false;

    this.updateUserForm.reset();
  }

  startLoading(): void {
    this.isLoading = true;
  }

  stopLoading(): void {
    this.isLoading = false;
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
    this.showForm('updateuser-form');
  }

}
