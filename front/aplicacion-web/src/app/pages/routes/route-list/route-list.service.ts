import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Cliente, Route, Vendedor } from '../routes.component';
import { environment } from '../../../../environments/environment';
import { catchError, finalize, Observable } from 'rxjs';
import { CreateRoute } from '../route-add/route-add.component';
import { AddStopToRoute, UpdateRoute } from '../stop-add/stop-add.component';

export type Parada = {
  cliente: Cliente
  vendedor: Vendedor
  fecha: string
  nombre: string
}

export type Ruta = {
  id: string
  inicio: string
  fin: string
  paradas: Parada[]
  nombre: string
}

@Injectable({
  providedIn: 'root'
})
export class RouteListService {

  private http = inject(HttpClient)

  constructor() { }

  getRoutes(){
    return this.http
    .get(`${environment.apiUrl}/api/rutas`)
    .pipe(
      catchError((e, source) => {
        console.error(e)
        console.error(source)
        return new Observable()
      }),
      finalize(() => console.error("finalized call")) 
    ) as unknown as Observable<Route[]>
  }

  
  getRoute(route_id: string){
    return this.http
    .get(`${environment.apiUrl}/api/rutas/${route_id}`)
    .pipe(
      catchError((e, source) => {
        console.error(e)
        console.error(source)
        return new Observable()
      }),
      finalize(() => console.error("finalized call"))
    )as unknown as Observable<Route>
  }

  generateRoute(body: CreateRoute) {
    return this.http
    .post(`${environment.apiUrl}/api/generate-route`, body)
    .pipe(
      catchError((e, source) => {
        console.error(e)
        console.error(source)
        return new Observable()
      }),
      finalize(() => console.error("finalized call"))
    )as unknown as Observable<Route>
  }

  updateRoute(body: UpdateRoute) {
    return this.http
    .put(`${environment.apiUrl}/api/update-route`, body)
    .pipe(
      catchError((e, source) => {
        console.error(e)
        console.error(source)
        return new Observable()
      }),
      finalize(() => console.error("finalized call"))
    )as unknown as Observable<Route>
  }

  addStopToRoute(body: AddStopToRoute) {
    return this.http
    .post(`${environment.apiUrl}/api/add-stop-route`, body)
    .pipe(
      catchError((e, source) => {
        console.error(e)
        console.error(source)
        return new Observable()
      }),
      finalize(() => console.error("finalized call"))
    )as unknown as Observable<Route>
  }

}
