import { Component, inject, Input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { GoogleMapsModule } from '@angular/google-maps';
import { Parada, RouteListService } from './route-list/route-list.service';
import { ActivatedRoute, Router } from '@angular/router';
import { MatTabsModule } from '@angular/material/tabs';
import { Observable } from 'rxjs';
import { AsyncPipe } from '@angular/common';

export type Cliente = { id: string, nombre: string, direccion: string }
export type Vendedor = Cliente

export type Route = {
  distancia: number
  id: string
  mapsResponse: any[]
  nombreRuta: string
  paradas: Parada[]
  tiempoEstimado: number
  fecha: string
  inicio: string
  fin: string
}

@Component({
  selector: 'app-routes',
  imports: [MatButtonModule, GoogleMapsModule, MatTabsModule, AsyncPipe],
  templateUrl: './routes.component.html',
  styleUrl: './routes.component.css'
})
export class RoutesComponent {

  private router: Router = inject(Router)
  private routesListService = inject(RouteListService)

  center: google.maps.LatLngLiteral = { lat: 4.7110, lng: -74.0721 };
  zoom = 12;

  Math = Math
  route!: Observable<Route>
  mapLoaded: Boolean = false
  encoding?: any
  LatLngBounds?: any
  @Input()
  route_id: string = ''

  constructor(private activatedRoute: ActivatedRoute) {
  }

  navigateTo(path: string) {
    this.router.url
    this.router.navigate([`${this.router.url}/${path}`])
  }

  ngOnInit() {
    this.route_id = this.activatedRoute.snapshot.paramMap.get("id") || ""
    this.route = this.getRoute()
    this.initMap()
  }

  getRoute() {
    return this.routesListService.getRoute(this.route_id)
  }

  async initMap(): Promise<void> {
    const { encoding } = await google.maps.importLibrary("geometry") as google.maps.GeometryLibrary;
    this.encoding = encoding
    this.mapLoaded = true
  }

  getPath(mapsResponse: any) {
    const encodedPolyline = mapsResponse[0]?.overview_polyline?.points
    const path = decodePathFromPolyline(encodedPolyline, this.encoding)
    return{ path, strokeColor: 'blue', strokeOpacity: 0.5, strokeWeight: 4 }
  }

  getMarkers(legs: any[]) {
    console.log(legs)
    return legs.map((leg, i) => {
      return {
        position: leg.start_location,
        title: leg.start_address,
        label: "" + i
      }
    })
  }

  getCenter(bounds: {northeast: {lat: number, lng: number}, southwest: {lat: number, lng: number}}){
    return new google.maps.LatLngBounds(
      bounds.southwest,
      bounds.northeast
    ).getCenter()
  }
  
  getZoom(bounds: {northeast: {lat: number, lng: number}, southwest: {lat: number, lng: number}}){
    return new google.maps.LatLngBounds(
      bounds.southwest,
      bounds.northeast
    ).toSpan()
  }

  fitBounds(route: Route, map: google.maps.Map) {
    const latlngBounds = new google.maps.LatLngBounds(
      route.mapsResponse[0].bounds.southwest,
      route.mapsResponse[0].bounds.northeast
    )
    map.fitBounds(latlngBounds)
  }

  drawRoutes(route: Route, map: google.maps.Map) {
    this.fitBounds(route, map)
  }

  getPedidoDuration([_, leg]: [Parada, any]) {
    return this.Math.round(leg.duration.value / 60)
  }

  getPedidoAndLeg(pedidos: Parada[], mapsResponse: any, pedidoPosition: number): [Parada, any] {
    const route = mapsResponse[0]
    const legs = route.legs
    const waypointPosition = route["waypoint_order"][pedidoPosition]
    return [pedidos[pedidoPosition], legs[waypointPosition]]
  }
}

function decodePathFromPolyline(polyline: any, encoding: any) {
  return encoding.decodePath(polyline)
}