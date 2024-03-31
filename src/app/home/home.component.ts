import { Component, OnInit } from '@angular/core';

import { UserService } from '../user.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  zipCode: number;

  constructor(private userService: UserService) {
    this.zipCode = this.userService.currentUser?.fiveDigitZip()!;
  }

  ngOnInit() {

  }

  updateZip(event: Event) {
    event.preventDefault();
    let inputElm = document.getElementById("zipCode") as HTMLInputElement
    this.zipCode = parseInt(inputElm!.value)
  }

  resetZip(event: Event) {
    event.preventDefault();
    this.zipCode = this.userService.currentUser?.fiveDigitZip()!;
  }

}
