/*
  Purpose: This component handles the restaurant widget of the application.
  Requirements: 1.1.0
*/
import { Component, Input, OnInit } from '@angular/core';
import { DataService } from 'src/app/data.service';
import { Restaurant } from '../../restaurant';
import { HttpClient } from '@angular/common/http';
import { Response } from 'src/app/response';
import { RestaurantResponse } from 'src/app/restaurant-response';

interface SimpleChanges {
  __index(zip: number): SimpleChanges
}

@Component({
  selector: 'app-restaurant-widget',
  templateUrl: './restaurant-widget.component.html',
  styleUrls: ['./restaurant-widget.component.css']
})
export class RestaurantWidgetComponent implements OnInit {

  constructor(private http: HttpClient) { }

  @Input() zipCode: number = 0;
  restaurantList: Restaurant[] | null = null;
  data: DataService = new DataService(this.http);

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.zipCode == 0) return;
    this.data.getRestaurants(this.zipCode).subscribe(res => {
      var response = <RestaurantResponse>(JSON.parse(res.body.Item.data));
      this.restaurantList = this.data.filterRestaurantsByZip(response.results, this.zipCode);
      console.log(this.restaurantList);
    });
  }

}
