import { Component, inject, Input, Output } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { GoogleMapsModule } from '@angular/google-maps';
import { Parada, Pedido, RouteListService } from '../route-list/route-list.service';
import { ActivatedRoute } from '@angular/router';

export type Cliente = {id: string, nombre: string, direccion: string}

export type Route = {
  distancia: number
  id: string
  mapsResponse: any[]
  nombreRuta: string
  pedidos: Parada[]
  tiempoEstimado: number
  fecha: string
}

@Component({
  selector: 'app-routes',
  imports: [MatButtonModule, GoogleMapsModule],
  templateUrl: './routes.component.html',
  styleUrl: './routes.component.css'
})
export class RoutesComponent {

  private routesListService = inject(RouteListService)
  
  center: google.maps.LatLngLiteral = {lat: 4.7110, lng: -74.0721};
  zoom = 12;

  Math = Math
  route?: Route
  route_path?: any
  mapMarkers?: any[]
  mapLoaded: Boolean = false
  encoding?: any
  LatLngBounds?: any
  @Input()
  route_id: string = ''

  constructor(private activatedRoute: ActivatedRoute) {
  }
  
  ngOnInit(){
    this.route_id = this.activatedRoute.snapshot.paramMap.get("id") || ""
    this.initMap()
    this.getRoute()
  }

  getRoute() {
    this.routesListService.getRoute(this.route_id).subscribe(this.parseRoute.bind(this))
  }

  parseRoute(route: Route) {
    this.route = route
  }

  async initMap(): Promise<void> {
    const {encoding} = await google.maps.importLibrary("geometry") as google.maps.GeometryLibrary;
    this.encoding = encoding
    this.mapLoaded = true
  }
  
  async getPath(mapsResponse: any) {
    const encodedPolyline = mapsResponse[0]?.overview_polyline?.points
    this.route_path = decodePathFromPolyline(encodedPolyline, this.encoding)
  }

  getMarkers(legs:any[]) {
    this.mapMarkers = legs.map(pedido => pedido.start_location)
  }

  onMapLoad(map: google.maps.Map) {
    this.fitBounds(map)
    this.drawRoutes(map)
  }
  
   fitBounds(map: google.maps.Map) {
    const latlngBounds = new google.maps.LatLngBounds(
      this.route!!.mapsResponse[0].bounds.southwest,
      this.route!!.mapsResponse[0].bounds.northeast
    )
    map.fitBounds(latlngBounds)
  }

  drawRoutes(map: google.maps.Map) {
    this.getMarkers(this.route!!.mapsResponse[0].legs)
    this.getPath(this.route!!.mapsResponse)
  }

  getPedidoDuration([_, leg]: [Parada, any]){
    return leg.duration.value
  }
  
  getPedidoAndLeg(pedidos: Parada[], mapsResponse:any, pedidoPosition: number): [Parada, any]{
    const route = mapsResponse[0]
    const legs = route.legs
    const waypointPosition = route["waypoint_order"][pedidoPosition]
    return [pedidos[pedidoPosition], legs[waypointPosition]]
  }
}

function decodePathFromPolyline(polyline: any, encoding: any) {
  return encoding.decodePath(polyline)
}