// fabricantes-listar/fabricantes-listar.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';


export type Fabricante = {
  id: number;
  nombre: string;
  imagen?: string;
};

@Injectable({
  providedIn: 'root'
})
export class FabricantesListarService {
  baseUrl = `${environment.apiUrl}`
  private apiUrl = `${this.baseUrl}/fabricantes`;
  //private apiUrl = 'http://compras.cppxcode.shop/api/fabricantes'; 
  constructor(private http: HttpClient) {}

  obtenerFabricantes(): Observable<Fabricante[]> {
    return this.http.get<Fabricante[]>(this.apiUrl);
  }
}
