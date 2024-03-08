import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { WidgetComponent } from './widget/widget.component';
import { CardComponent } from './card/card.component';
import { WeatherComponent } from './weather/weather.component';
import { SigninComponent } from './signin/signin.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './home/home.component';



@NgModule({
  declarations: [
    AppComponent,
    WidgetComponent,
    CardComponent,
    WeatherComponent,
    SigninComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule, HttpClientModule, AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { 

}
