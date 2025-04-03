import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Cliente, Route } from '../routes/routes.component';
import { environment } from '../../../environments/environment';
import { catchError, finalize, Observable } from 'rxjs';

export type Parada = {
  direccion: string
  cliente: Cliente
  fecha: Date
  nombre: string
}

export type Pedido = {
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
    .get(`${environment.apiUrl}/route`)
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
    .get(`${environment.apiUrl}/route/${route_id}`)
    .pipe(
      catchError((e, source) => {
        console.error(e)
        console.error(source)
        return new Observable()
      }),
      finalize(() => console.error("finalized call"))
    )as unknown as Observable<Route>
  }

  generateRoute(body: {pedidos: Parada[]}) {
    return this.http
    .post(`${environment.apiUrl}/generate_route`, body)
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
