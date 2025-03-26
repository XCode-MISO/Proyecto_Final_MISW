from datetime import datetime
import googlemaps
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import os
import pybreaker

# Used in database integration points
maps_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

api_key = os.environ.get('GMAPS_API_KEY', "")
gmaps = googlemaps.Client(key=api_key)

@maps_breaker
def getRouteFromListOfRoutes(routes, mode="driving", departure_time=datetime.now()):
  return gmaps.directions(
        routes[0], 
        routes[0],
        waypoints=routes[1:], 
        optimize_waypoints=True, 
        mode=mode, 
        departure_time=departure_time
    )
  origins = [routes[0]]
  destinations = routes[1:]
  
  # Distance matrix
  data = {}
  data["distance_matrix"] = gmaps.distance_matrix(
        origins,
        destinations,
        mode,
        departure_time
     )
  data["depot"] = 0
  data["num_vehicles"] = 1
  
  manager = pywrapcp.RoutingIndexManager(
      len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
  )
  
  routing = pywrapcp.RoutingModel(manager)

  def distance_callback(from_index, to_index):
      """Returns the distance between the two nodes."""
      # Convert from routing variable Index to distance matrix NodeIndex.
      from_node = manager.IndexToNode(from_index)
      to_node = manager.IndexToNode(to_index)
      return data["distance_matrix"]["rows"][from_node]["elements"][to_node-1]

  transit_callback_index = routing.RegisterTransitCallback(distance_callback)

  # Define cost of each arc.
  routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

  # Setting first solution heuristic.
  search_parameters = pywrapcp.DefaultRoutingSearchParameters()
  search_parameters.first_solution_strategy = (
      routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
  )

  # Solve the problem.
  solution = routing.SolveWithParameters(search_parameters) 
  return solution
