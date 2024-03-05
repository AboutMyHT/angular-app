import { Component } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'aboutmyhometown.com';

  apiUrl: string = environment.apiUrl;
  mainUrl: string = environment.mainUrl;

}
