/*
  Purpose: This component handles the home page of the application.
  Requirements: 4.1.x
*/
import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Globals } from '../globals.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  zipCode: number;
  public lat = "";
  public lng = "";

  constructor(private userService: UserService, private http: HttpClient, public globals: Globals) {
    this.zipCode = this.userService.currentUser?.fiveDigitZip()!;
  }

  ngOnInit() {

  }

  getLocation(e: Event) {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position: any) => {
        if (position) {
          console.log("Latitude: " + position.coords.latitude +
            "Longitude: " + position.coords.longitude);
          this.lat = position.coords.latitude.toString();
          this.lng = position.coords.longitude.toString();
          console.log(this.lat);
          console.log(this.lng);
          this.getZip(this.lat, this.lng).subscribe(res => {
            this.zipCode = parseInt(res['body']);
            this.globals.zipCode = this.zipCode;
            (document.getElementById("zipCode") as HTMLInputElement)!.value = "";
          });
        }
      },
        (error: any) => console.log(error));
    } else {
      alert("Geolocation is not supported by this browser.");
    }
  }

  getZip(lat: string, lng: string): Observable<{ "statusCode": number, "body": string }> {
    let postBody = {
      "lat": lat,
      "lng": lng
    }
    let url = "https://uoubgrd2cl.execute-api.us-east-2.amazonaws.com/dev"
    return this.http.post<{ "statusCode": number, "body": string }>(url, postBody)
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
