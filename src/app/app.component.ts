import { Component } from '@angular/core';

import { UserService } from './user.service';
import { User } from './user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  isLoggedIn: boolean;
  user: User;

  constructor(userService: UserService) {
    this.isLoggedIn = userService.isLoggedIn();

    this.user = userService.currentUser!;
  }

  signout() {
    localStorage.removeItem('sessionToken');
    window.location.reload();
  }
}
