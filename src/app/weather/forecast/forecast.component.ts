import { Component, OnInit } from '@angular/core';
import { Globals } from 'src/app/globals.service';
import { WeatherData } from 'src/app/weather-data';
import { UserService } from 'src/app/user.service';
import { HttpClient } from '@angular/common/http';
import { DataService } from 'src/app/data.service';
import { Response } from 'src/app/response';

@Component({
  selector: 'app-forecast',
  templateUrl: './forecast.component.html',
  styleUrls: ['./forecast.component.css']
})
export class ForecastComponent implements OnInit {
  zipCode: number;
  weather: WeatherData | null = null;

  constructor(private userService: UserService, private data: DataService) {
    this.zipCode = 90210;
   }


  ngOnInit(): void {
    this.data.getWeather(this.zipCode).subscribe(res => {
      var response: Response = <Response>res;
      this.weather = <WeatherData>(JSON.parse(response.body.Item.data));
      console.log(this.weather);
    });
  }

  viewData() {
    console.log(this.weather);
  }

  getIcon(url: string) {
    let iconList = url.split("/");
    return (`../assets/weathericons/${iconList[iconList.length - 2]}/${iconList[iconList.length - 1]}`)
  }

}
