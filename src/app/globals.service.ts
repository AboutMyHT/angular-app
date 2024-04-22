import { Injectable } from '@angular/core';
import { WeatherData } from './weather-data';

@Injectable({
  providedIn: 'root'
})


export class Globals {

  weather: WeatherData | null = null;
  zipCode: number = 0;

}
