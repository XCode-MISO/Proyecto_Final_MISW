import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, catchError, finalize, of } from 'rxjs';

export interface Inventario {
  producto_id: number;
  nombre: string;
  bodega: string;
  cantidad: number;
}

export interface DetalleInventarioProducto {
  producto_id: number;
  nombre: string;
  precio: number;
  moneda: string;
  stock: number;
  bodega: string;
  estante: string;
  pasillo: string;
}

@Injectable({
  providedIn: 'root'
})
export class InventarioListService {
  apiUrl = `https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api`;
  private http = inject(HttpClient);

  getInventario(): Observable<Inventario[]> {
    return this.http.get<Inventario[]>(`${this.apiUrl}/inventarios/ubicacion`).pipe(
      catchError((e) => {
        console.error(e);
        return of([]);
      }),
      finalize(() => console.log('Inventario cargado'))
    );
  }

  getInventarioId(product_id: number): Observable<DetalleInventarioProducto> {
    return this.http.get<DetalleInventarioProducto>(`${this.apiUrl}/inventarios/${product_id}`).pipe(
      catchError((e) => {
        console.error(e);
        return of({} as DetalleInventarioProducto);
      }),
      finalize(() => console.log('Detalle cargado'))
    );
  }
}
