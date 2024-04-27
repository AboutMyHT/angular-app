import { Restaurant } from "./restaurant"

export interface RestaurantResponse {
    "summary": {
        "query": string
        "queryType": string
        "queryTime": number
        "numResults": number
        "offset": number
        "totalResults": number
        "fuzzyLevel": number
        "geoBias": {
          "lat": number
          "lon": number
        }
      },
      "results": Restaurant[]
}
