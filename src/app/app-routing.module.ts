/*
  Purpose: This component handles static application routing.
  Requirements: 4.x; 4.1.1; 4.2.1; 4.3.1; 4.5.1; 4.6.1; 4.7.x;
*/
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { authGuard } from './auth.guard';
import { guestGuard } from './guest.guard';

import { SigninComponent } from './signin/signin.component';
import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';
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
