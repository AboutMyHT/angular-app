import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { APP_INITIALIZER } from '@angular/core';

import { UserService } from './user.service';

import { AppComponent } from './app.component';
import { SigninComponent } from './signin/signin.component';
import { ProfileComponent } from './profile/profile.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './home/home.component';
import { WeatherWidgetComponent } from './weather/weather-widget/weatherwidget.component';
import { WeatherForecastComponent } from './weather/weather-forcast/weatherforecast.component';
import { Globals } from './globals.service';
import { RestaurantsComponent } from './restaurant/restaurants/restaurants.component';
import { RestaurantWidgetComponent } from './restaurant/restaurant-widget/restaurant-widget.component';

@NgModule({
  declarations: [
    AppComponent,
    SigninComponent,
    ProfileComponent,
    HomeComponent,
    WeatherWidgetComponent,
    WeatherForecastComponent,
    RestaurantsComponent,
    RestaurantWidgetComponent
  ],
  imports: [
    BrowserModule, HttpClientModule, AppRoutingModule, ReactiveFormsModule
  ],
  providers: [{
    provide: APP_INITIALIZER,
    useFactory: (userService: UserService) => () => userService.initializeUser(),
    deps: [UserService],
    multi: true
  },
    Globals
  ],
  bootstrap: [AppComponent]
})

export class AppModule {

}
