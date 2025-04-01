import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { routesMock } from './mock/route.mock';
import { GoogleMapsModule } from '@angular/google-maps';

export type Route = {
  distancia: number
  id: string
  mapsResponse: any
  nombreRuta: string
  pedidos: Array<{id: string, direccion: string, legs: any}>
  tiempoEstimado: number
  client: {id: string, nombre: string}
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
  routes: Route[] = routesMock
  route?: any
  mapMarkers?: any[]

  constructor() {
    this.getPath(routesMock[0].mapsResponse)
  }

  async getPath(mapsResponse: any) {
    const encodedPolyline = mapsResponse[ 0 ]?.overview_polyline?.points
    const { encoding } = google.maps.importLibrary('geometry') as google.maps.GeometryLibrary;

    this.route = encoding.decodePath(encodedPolyline)
  }
}
