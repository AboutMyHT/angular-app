/*
  Purpose: This component handles the page not found page of the application.
  Requirements: 4.7.x
*/
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-page-not-found',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './page-not-found.component.html',
  styleUrls: ['./page-not-found.component.css']
})
export class PageNotFoundComponent {
}
