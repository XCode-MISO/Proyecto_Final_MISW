import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Fabricante } from './fabricantes-crear.component';
import { environment } from '../../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FabricantesCrearService {
  private readonly apiUrl = `${environment.apiUrl}/api/fabricantes`;
  constructor(private http: HttpClient) {}

  crearFabricante(fabricante: Fabricante): Observable<Fabricante> {
    return this.http.post<Fabricante>(this.apiUrl, fabricante);
  }
}