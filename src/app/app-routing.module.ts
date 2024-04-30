import { NgModule } from '@angular/core';
// import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { authGuard } from './auth.guard';
import { guestGuard } from './guest.guard';

import { SigninComponent } from './signin/signin.component';
import { AboutComponent } from './about/about.component';
// import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
// import { WeatherComponent } from './weather/weather.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { ProfileComponent } from './profile/profile.component';
import { WeatherForecastComponent } from './weather/weather-forcast/weatherforecast.component';
import { RestaurantsComponent } from './restaurant/restaurants/restaurants.component';



const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, canActivate: [authGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [authGuard] },
  { path: 'about', component: AboutComponent },
  { path: 'signin', component: SigninComponent, canActivate: [guestGuard] },
  { path: 'forecast', component: WeatherForecastComponent, canActivate: [authGuard] },
  { path: 'restaurants', component: RestaurantsComponent, canActivate: [authGuard] },
  { path: '**', component: PageNotFoundComponent }
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
