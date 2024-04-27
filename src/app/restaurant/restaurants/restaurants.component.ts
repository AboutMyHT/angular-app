import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Restaurant } from '../../restaurant';
import { DataService } from '../../data.service';
import { RestaurantResponse } from '../../restaurant-response';

@Component({
  selector: 'app-restaurants',
  templateUrl: './restaurants.component.html',
  styleUrls: ['./restaurants.component.css']
})


export class RestaurantsComponent implements OnInit {

  constructor(private http: HttpClient, private route: ActivatedRoute) { }

  restaurantList: Restaurant[] | null = null;
  restaurantMasterList: Restaurant[] | null = null;
  restaurantURL: Map<string, string> = new Map<string, string>();
  categoryList: string[] | null = null;
  zipCode: number = 0;
  data: DataService = new DataService(this.http);

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.zipCode = params['zipCode'];
      if (!this.zipCode) {
        window.location.href = "/"
      }
    })
    this.data.getRestaurants(this.zipCode).subscribe(res => {
      var response = <RestaurantResponse>(JSON.parse(res.body.Item.data));
      this.restaurantList = this.data.filterRestaurantsByZip(response.results, this.zipCode);
      this.restaurantMasterList = this.restaurantList!;
      this.categoryList = (this.data.getRestaurantCategories(this.restaurantList!)).sort();
      this.categoryList.unshift("All");
    });
  }

  onFilter(filter: string) {
    if (filter == 'All') {
      this.restaurantList = this.restaurantMasterList;
    } else {
      this.restaurantList = this.data.filterRestaurantsByCategory(this.restaurantMasterList!, filter);
    }
  }

  onSort(event: Event) {
    let currElm = event.currentTarget as HTMLElement
    if (currElm.textContent == 'Name') {
      this.restaurantList!.sort(function (a: Restaurant, b: Restaurant) { return (a.poi.name.localeCompare(b.poi.name)) });
    } else if (currElm.textContent == 'Category') {
      this.restaurantList!.sort((a: Restaurant, b: Restaurant) => { return (this.data.getRestaurantCategory(a).localeCompare(this.data.getRestaurantCategory(b))) });
    }
  }

}
