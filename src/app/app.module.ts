import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { WidgetComponent } from './widget/widget.component';
import { CardComponent } from './card/card.component';

@NgModule({
  declarations: [
    AppComponent,
    WidgetComponent,
    CardComponent
  ],
  imports: [
    BrowserModule, HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
