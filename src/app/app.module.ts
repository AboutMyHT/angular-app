import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { APP_INITIALIZER } from '@angular/core';

import { UserService } from './user.service';

import { AppComponent } from './app.component';
import { WidgetComponent } from './widget/widget.component';
import { CardComponent } from './card/card.component';
import { WeatherComponent } from './weather/weather.component';
import { SigninComponent } from './signin/signin.component';
import { ProfileComponent } from './profile/profile.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './home/home.component';
import { CurrentComponent } from './weather/current/current.component';
import { ForecastComponent } from './weather/forecast/forecast.component';
import { Globals } from './globals.service';




@NgModule({
  declarations: [
    AppComponent,
    WidgetComponent,
    CardComponent,
    WeatherComponent,
    SigninComponent,
    ProfileComponent,
    HomeComponent,
    CurrentComponent,
    ForecastComponent
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
