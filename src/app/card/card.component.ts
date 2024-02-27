import { Component, OnInit, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {
  data: any;

  @Input() header: string = '';
  @Input() title: string = '';
  @Input() subtitle: string = '';
  @Input() body: string = "";
  @Input() footer: string = "";

  @Input() btnPrimaryText: string = "";
  @Input() btnPrimaryLink: string = "";
  @Input() btnSecondaryText: string = "";
  @Input() btnSecondaryLink: string = "";

  @Input() cardImgURL: string = "";

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getData();
  }

  getData(): void {
    this.http.get('https://httpbin.org/get').subscribe(data => {
      this.data = data;
    });
  }

}
