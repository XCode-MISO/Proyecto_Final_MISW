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
  moneda: string;
  bodega: string;     
  estante: string;       
  pasillo: string; 
}

@Injectable({ providedIn: 'root' })
export class ProductosService {
  private readonly apiUrl = `${environment.apiUrl}/api`;

  constructor(private http: HttpClient) {}


  obtenerFabricantes(): Observable<FabricanteDto[]> {
    return this.http.get<FabricanteDto[]>(`${this.apiUrl}/fabricantes`);
  }

  cargarProducto(prod: ProductoDto): Observable<void> {
    return this.http.post<void>(`${this.apiUrl}/productos`, prod);
  }
}