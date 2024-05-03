import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';


import { WeatherWidgetComponent } from './weatherwidget.component';

describe('CurrentComponent', () => {
  let component: WeatherWidgetComponent;
  let fixture: ComponentFixture<WeatherWidgetComponent>;

  
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [WeatherWidgetComponent],
      imports: [HttpClientTestingModule]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WeatherWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

});
