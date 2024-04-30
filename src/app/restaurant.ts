export interface Restaurant {
    "type": string
    "id": string
    "score": number
    "dist": number
    "info": string
    "poi": {
        "name": string
        "phone": string
        "url": string
        "categorySet": [
            {
                "id": number
            }
        ],
        "categories": string[]
        "classifications":
        {
            "code": string
            "names":
            {
                "nameLocale": string
                "name": string
            }[]
        }[],
        "openingHours": {
            "timeRanges": {
                "startTime": {
                    "date": string
                    "hour": number
                    "minute": number
                },
                "endTime": {
                    "date": string
                    "hour": number
                    "minute": number
                }[]
            }
        }
    },
    "address": {
        "streetNumber": string
        "streetName": string
        "municipality": string
        "countrySecondarySubdivision": string
        "countrySubdivision": string
        "countrySubdivisionName": string
        "countrySubdivisionCode": string
        "postalCode": string
        "extendedPostalCode": string
        "countryCode": string
        "country": string
        "countryCodeISO3": string
        "freeformAddress": string
        "localName": string
    },
    "position": {
        "lat": number
        "lon": number
    },
    "viewport": {
        "topLeftPoint": {
            "lat": number
            "lon": number
        },
        "btmRightPoint": {
            "lat": number
            "lon": number
        }
    },
    "entryPoints": [
        {
            "type": string,
            "position": {
                "lat": number
                "lon": number
            }
        }
    ]
}
