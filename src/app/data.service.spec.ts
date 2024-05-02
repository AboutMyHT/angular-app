import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { DataService } from './data.service';
import { Restaurant } from './restaurant';

describe('DataService', () => {
  let service: DataService;
  let r: Restaurant[] = [
    {
      "type": "POI",
      "id": "gLnQVw_YyrJpqB7aiyh2wQ",
      "score": 2.8261345284,
      "dist": 4069.645063,
      "info": "search:ta:840171000723000-US",
      "poi": {
        "name": "Miss Barlow's Cafe",
        "phone": "+1 217-382-5782",
        "categorySet": [
          {
            "id": 7315
          }
        ],
        "url": "missbarlowscafe.yolasite.com",
        "categories": [
          "restaurant"
        ],
        "classifications": [
          {
            "code": "RESTAURANT",
            "names": [
              {
                "nameLocale": "en-US",
                "name": "restaurant"
              }
            ]
          }
        ]
      },
      "address": {
        "streetNumber": "31",
        "streetName": "West Cumberland Street",
        "municipality": "Martinsville",
        "countrySecondarySubdivision": "Clark",
        "countrySubdivision": "IL",
        "countrySubdivisionName": "Illinois",
        "countrySubdivisionCode": "IL",
        "postalCode": "62442",
        "extendedPostalCode": "62442-1190",
        "countryCode": "US",
        "country": "United States",
        "countryCodeISO3": "USA",
        "freeformAddress": "31 West Cumberland Street, Martinsville, IL 62442",
        "localName": "Martinsville"
      },
      "position": {
        "lat": 39.332852,
        "lon": -87.882824
      },
      "viewport": {
        "topLeftPoint": {
          "lat": 39.33375,
          "lon": -87.88399
        },
        "btmRightPoint": {
          "lat": 39.33195,
          "lon": -87.88166
        }
      },
      "entryPoints": [
        {
          "type": "main",
          "position": {
            "lat": 39.33305,
            "lon": -87.88292
          }
        }
      ]
    }
  ]

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [DataService]
    });
    service = TestBed.inject(DataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return a dow', () => {
    expect(service.getDOW('2024-02-20 6:08')).toBe('Wen');
  });

  it('should return phone number', () => {
    expect(service.getRestaurantPhone(r[0])).toBe('217-382-5782');
  });

  it('should return restaurants catagories', () => {
    expect(service.getRestaurantCategories(r)).toContain('restaurant');
  });

  it('should return restaurant category', () => {
    expect(service.getRestaurantCategory(r[0])).toBe('restaurant');
  });


});
