import { Component, Input } from '@angular/core';
import { CurrentComponent } from './current/current.component';

@Component({
  selector: 'app-weather',
  templateUrl: './weather.component.html',
  styleUrls: ['./weather.component.css']
})
export class WeatherComponent {

  @Input() zipCode: number = 0;


}
