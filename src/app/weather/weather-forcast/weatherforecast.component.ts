import { Component, OnInit } from '@angular/core';
import { Globals } from 'src/app/globals.service';
import { WeatherData } from 'src/app/weather-data';
import { UserService } from 'src/app/user.service';
import { HttpClient } from '@angular/common/http';
import { DataService } from 'src/app/data.service';
import { Response } from 'src/app/response';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-weatherforecast',
  templateUrl: './weatherforecast.component.html',
  styleUrls: ['./weatherforecast.component.css']
})
export class WeatherForecastComponent implements OnInit {
  zipCode: number = 0;
  weather: WeatherData | null = null;

  constructor(private userService: UserService, private data: DataService, private route: ActivatedRoute) {
    // this.zipCode = this.userService.currentUser?.fiveDigitZip()!;
  }


  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.zipCode = params['zipCode'];
      if (!this.zipCode) {
        window.location.href = "/"
      }
    })
    this.data.getWeather(this.zipCode).subscribe(res => {
      var response: Response = <Response>res;
      this.weather = <WeatherData>(JSON.parse(response.body.Item.data));
      console.log(this.weather);
    });
  }

  getIcon(url: string) {
    let iconList = url.split("/");
    return (`../assets/weathericons/${iconList[iconList.length - 2]}/${iconList[iconList.length - 1]}`)
  }

  getDayOfWeek(epoch_time: number) {
    let a = new Date(epoch_time * 1000);
    let days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    return days[a.getDay()];
  }

}
