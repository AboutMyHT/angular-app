import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { RestaurantWidgetComponent } from './restaurant-widget.component';

describe('RestaurantsComponent', () => {
  let component: RestaurantWidgetComponent;
  let fixture: ComponentFixture<RestaurantWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RestaurantWidgetComponent ],
      imports: [HttpClientTestingModule, RouterTestingModule]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RestaurantWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
