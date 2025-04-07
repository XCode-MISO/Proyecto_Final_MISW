import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';

export interface FabricanteDto {
  id: number;
  nombre: string;
}

export interface ProductoDto {
  nombre: string;
  fabricanteId: number;
  cantidad: number;
  precio: number;
}

@Injectable({ providedIn: 'root' })
export class ProductosService {
  private readonly apiUrl = `https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/compras`;

  constructor(private http: HttpClient) {}


  obtenerFabricantes(): Observable<FabricanteDto[]> {
    return this.http.get<FabricanteDto[]>(`${this.apiUrl}/fabricantes`);
  }

  cargarProducto(prod: ProductoDto): Observable<void> {
    return this.http.post<void>(`${this.apiUrl}/compras/detalle`, prod);
  }
}