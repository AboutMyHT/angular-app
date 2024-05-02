import { Injectable } from '@angular/core';
import { Observable, filter } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Response } from './response';
import { Restaurant } from './restaurant';

@Injectable({
    providedIn: 'root'
})

export class DataService {

    apiGatewayURL = "https://aqw8pgiwx8.execute-api.us-east-2.amazonaws.com/prod"

    constructor(private http: HttpClient) { }

    getWeather(zip: number): Observable<Response> {
        let postBody = {
            "table": "apidata",
            "type": "weather",
            "zip": zip
        }
        return this.http.post<Response>(this.apiGatewayURL, postBody);
    }

    getRestaurants(zip: number): Observable<Response> {
        let postBody = {
            "table": "apidata",
            "type": "restaurants",
            "zip": zip
        }
        return this.http.post<Response>(this.apiGatewayURL, postBody);
    }

    getRestaurantPhone(r: Restaurant): string {
        if (!r.poi.phone) {
            return ""
        }
        let phoneParts = r.poi.phone.split(" ");
        if (phoneParts.length > 1) {
            return phoneParts[1];
        }
        return ""
    }

    filterRestaurantsByZip(restaurants: Restaurant[], zip: number): any {
        let filteredRestaurants = restaurants.filter(r => Number(r.address.postalCode) == zip)
        return filteredRestaurants
    }

    filterRestaurantsByCategory(restaurants: Restaurant[], category: string): any {
        let filteredRestaurants = restaurants.filter(r => this.getRestaurantCategory(r) == category)
        filteredRestaurants.join('restaurant')
        return filteredRestaurants
    }

    getRestaurantCategories(restaurant: Restaurant[]): string[] {
        let response = new Set(restaurant.map(r => this.getRestaurantCategory(r)));
        return Array.from(response);
    }

    getRestaurantCategory(restaurant: Restaurant): string {
        let response = restaurant.poi.categories.filter(c => c != 'restaurant');
        if (response.length > 0) {
            return response[0];
        }
        return "restaurant";
    }

    getDOW(date: string) {
        //date in format "2024-02-20 6:08"
        const days = ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun']
        return (days[(new Date(date)).getDay()])
    }

}
