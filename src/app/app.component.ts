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
  currentUser: User;
  title = 'aboutmyhometown.com';

  constructor(userService: UserService) {
    this.isLoggedIn = userService.isLoggedIn();

    this.currentUser = userService.currentUser!;
  }

  signout() {
    localStorage.removeItem('sessionToken');
    window.location.reload();
  }
}
