import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  // cardtitle = "Litchfield, IL.";
  // cardsubtitle = "Current Weather";
  zip = 62701;
  ngOnInit() {

  }

  updateZip(event: Event) {
    event.preventDefault();
    let inputElm = document.getElementById("zipCode") as HTMLInputElement
    this.zip = parseInt(inputElm!.value)
  }

}
