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
  //private apiUrl = 'https://67f142f7c733555e24aca5a3.mockapi.io/misw-pruebas/fabricantes';
  private readonly apiUrl = `https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/fabricantes`;
  constructor(private http: HttpClient) {}

  obtenerFabricantes(): Observable<Fabricante[]> {
    return this.http.get<Fabricante[]>(this.apiUrl);
  }
}