import { Component } from '@angular/core';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {

  action = "signin"

  forgotPassword(event: Event) {
    event.preventDefault();
    this.action = "forgot";
    this.displayForm();
  }

  onClick(event: Event) {
    let elementId: string = (event.target as Element).id;
    console.log(elementId);
    event.preventDefault();
    if (elementId == "register") {
      if (this.action == "register") {
        this.action = "signin";
      } else {
        this.action = "register";
      }
    } else if (elementId == "forgot") {
      if (this.action == "forgot") {
        this.action = "signin";
      } else {
      this.action = "forgot";
      }
    }
    this.displayForm();
  }

  signUp(event: Event) {  
    event.preventDefault();
  }

  displayForm() {
    const messageElm = document.getElementById("emailMessage") as HTMLElement;
    const passwordElm = document.getElementById("pswGroup") as HTMLInputElement;
    const submitElm = document.getElementById("submitButton") as HTMLInputElement;
    const actionElm = document.getElementById("actionText") as HTMLInputElement;
    const regGroupElm = document.getElementById("regGroup") as HTMLElement;
    const forgotElm = document.getElementById("forgot") as HTMLElement;
    const donthaveElm = document.getElementById("donthave") as HTMLElement;
    const registerElm = document.getElementById("register") as HTMLElement;


    if (this.action == "forgot") {
      messageElm.style.display = "inherit";
      passwordElm.style.display = "none";
      forgotElm.innerText = "Back to Sign In"
      submitElm.innerText = "Send Password Reset Link"
      actionElm.innerText = "Reset Password"

    } else if (this.action == "register") {
      messageElm.style.display = "none";
      regGroupElm.style.display = "inherit";
      submitElm.innerText = "Register"
      actionElm.innerText = "Register"
      forgotElm.style.display = "none";
      passwordElm.style.display = "inherit";
      donthaveElm.innerText = "Already have an account? "
      registerElm.innerText = "Sign In"
    } else {
      messageElm.style.display = "none";
      regGroupElm.style.display = "none";
      forgotElm.innerText = "Forgot your password?"
      forgotElm.style.display = "inherit";
      passwordElm.style.display = "inherit";
      donthaveElm.innerText = "Don't have an account? "
      registerElm.innerText = "Sign up here"
      submitElm.innerText = "Sign In"
      actionElm.innerText = "Sign In"
    }
  }

  submit(event: Event) {
  
  }
}
