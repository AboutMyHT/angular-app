import { Component, OnInit, Input } from '@angular/core';
import { DataService } from 'src/app/data.service';
import { WeatherData } from 'src/app/weather-data';
import { HttpClient } from '@angular/common/http';
import { Response } from 'src/app/response';
import { CityData } from 'src/app/city-data'
import { Globals } from 'src/app/globals.service';

interface SimpleChanges {
  __index(zip: number): SimpleChanges
}


@Component({
  selector: 'app-weatherwidget',
  templateUrl: './weatherwidget.component.html',
  styleUrls: ['./weatherwidget.component.css']
})
export class WeatherWidgetComponent implements OnInit {

  constructor(private http: HttpClient) { }

  @Input() zipCode: number = 0;
  data = new DataService(this.http);
  weather: WeatherData | null = null;

  ngOnInit() { }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.zipCode == 0) {
      return;
    }
    this.data.getWeather(this.zipCode).subscribe(res => {
      var response: Response = <Response>res;
      this.weather = <WeatherData>(JSON.parse(response.body.Item.data));
    });
  }


  getTemp(units: string) {
    if (units == 'c') {
      return (this.weather!.current.temp_c + "\xB0C");
    } else {
      return (this.weather!.current.temp_f + "\xB0F");
    }
  }

  getFeelsLike(units: string) {
    if (units == 'c') {
      return (this.weather!.current.feelslike_c + "\xB0C");
    } else {
      return (this.weather!.current.feelslike_f + "\xB0F");
    }
  }

  getIcon(url: string) {
    let iconList = url.split("/");
    return (`../assets/weathericons/${iconList[iconList.length - 2]}/${iconList[iconList.length - 1]}`)
  }
}
