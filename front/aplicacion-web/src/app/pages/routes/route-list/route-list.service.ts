import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Cliente, Route, Vendedor } from '../routes.component';
import { catchError, finalize, Observable } from 'rxjs';
import { CreateRoute } from '../route-add/route-add.component';
import { AddStopToRoute, UpdateRoute } from '../stop-add/stop-add.component';
import { environment } from '../../../../environments/environment';

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
  headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  apiUrl = `${environment.apiUrl}`

  private http = inject(HttpClient)

  constructor() { }

  getRoutes() {

    return this.http
      .get(`${this.apiUrl}/api/rutas`, { headers:this.headers })
      .pipe(
        catchError((e, source) => {
          console.error(e);
          console.error(source);
          return new Observable();
        }),
        finalize(() => console.error("finalized call"))
      ) as unknown as Observable<Route[]>;
  }

  
  getRoute(route_id: string){
    return this.http
    .get(`${this.apiUrl}/api/rutas/${route_id}`, { headers:this.headers })
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
    .post(`${this.apiUrl}/api/generate-route`, body, { headers:this.headers })
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
    .put(`${this.apiUrl}/api/update-route`, body, { headers:this.headers })
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
    .post(`${this.apiUrl}/api/add-stop-route`, body, { headers:this.headers })
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
