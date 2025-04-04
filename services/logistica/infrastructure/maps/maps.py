from datetime import datetime
from typing import List
import uuid
import googlemaps
import os
import pybreaker

from logistica.infrastructure.maps.types import Bounds, Distance, Duration, Leg, Location, TypedObject

# Used in database integration points
maps_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

api_key = os.environ.get('GMAPS_API_KEY', "")
gmaps = googlemaps.Client(key=api_key)

def parse_json(json_data) -> List[TypedObject]:
    if json_data == None:
        return [TypedObject(bounds=[], legs=[])]
    parsed_objects = []
    for item in json_data:
        bounds = Bounds(
            Location(item['bounds']['northeast']['lat'], item['bounds']['northeast']['lng']),
            Location(item['bounds']['southwest']['lat'], item['bounds']['southwest']['lng'])
        )
        legs = []
        for leg in item['legs']:
            distance = Distance(leg['distance']['text'], leg['distance']['value'])
            duration = Duration(leg['duration']['text'], leg['duration']['value'])
            end_location = Location(leg['end_location']['lat'], leg['end_location']['lng'])
            start_location = Location(leg['start_location']['lat'], leg['start_location']['lng'])
            legs.append(Leg(distance, duration, leg['end_address'], end_location, leg['start_address'], start_location))
        parsed_objects.append(TypedObject(bounds, legs))
    return parsed_objects

@maps_breaker
def getRouteFromMaps(start,end, routes, mode="driving"):
  if len(routes) < 1:
      return None
  return gmaps.directions(
        start, 
        end,
        waypoints=routes, 
        optimize_waypoints=True, 
        mode=mode
    )