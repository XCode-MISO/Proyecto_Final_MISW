import { Component, Output } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { routesMock } from './mock/route.mock';
import { GoogleMapsModule } from '@angular/google-maps';

export type Route = {
  distancia: number
  route_id: string
  mapsResponse: any
  nombreRuta: string
  pedidos: Array<{
    pedido_id: string, 
    direccion: string, 
    leg: any
    client: {id: string, nombre: string}
  }>
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
  
  center: google.maps.LatLngLiteral = {lat: 4.7110, lng: -74.0721};
  zoom = 12;

  Math = Math
  routes = routesMock[0].pedidos
  route?: any
  mapMarkers?: any[]
  mapLoaded: Boolean = false
  encoding?: any
  LatLngBounds?: any

  constructor() {
    this.getMarkers(routesMock[0].pedidos)
  }

  ngOnInit() {
    this.initMap()
  }

  async initMap(): Promise<void> {
    const {encoding} = await google.maps.importLibrary("geometry") as google.maps.GeometryLibrary;
    this.encoding = encoding
    this.mapLoaded = true
    this.getPath(routesMock[0].mapsResponse)
  }
  
  async getPath(mapsResponse: any) {
    const encodedPolyline = mapsResponse[ 0 ]?.overview_polyline?.points
    this.route = decodePathFromPolyline(encodedPolyline, this.encoding)
  }

  getMarkers(pedidos:any[]) {
    this.mapMarkers = pedidos.map(pedido => pedido.leg.start_location)
  }

  onMapLoad(map: google.maps.Map) {
    this.fitBounds(map)
    this.drawRoutes(map)
  }
  
  fitBounds(map: google.maps.Map) {
    const latlngBounds = new google.maps.LatLngBounds(
      routesMock[0].mapsResponse[0].bounds.southwest,
      routesMock[0].mapsResponse[0].bounds.northeast
    )
    map.fitBounds(latlngBounds)
  }

  drawRoutes(map: google.maps.Map) {
  }

}

function decodePathFromPolyline(polyline: any, encoding: any) {
  return encoding.decodePath(polyline)
}