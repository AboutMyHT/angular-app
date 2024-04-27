import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { HttpClient, HttpContext, HttpHeaders } from '@angular/common/http';
import { Response } from './response';
import { Restaurant } from './restaurant';


@Injectable({
    providedIn: 'root'
})
export class DataService {

    lambdaURL = "https://zxrppsvwue.execute-api.us-east-2.amazonaws.com/dev"

    constructor(private http: HttpClient) { }

    getWeather(zip: number): Observable<Response> {
        let postBody = {
            "table": "apidata",
            "type": "weather",
            "zip": zip
        }
        return this.http.post<Response>(this.lambdaURL, postBody);
    }

    getCity(zip: number): Observable<Response> {
        let postBody = {
            "table": "apidata",
            "type": "city",
            "zip": zip
        }
        return this.http.post<Response>(this.lambdaURL, postBody);
    }

    getRestaurants(zip: number): Observable<Response> {
        let postBody = {
            "table": "apidata",
            "type": "restaurants",
            "zip": zip
        }
        return this.http.post<Response>(this.lambdaURL, postBody).pipe(tap(res =>
            console.log(res)))
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
