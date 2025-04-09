import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

export type RegistrarVendedorResponse = {
  id: string
  createdAt: string
}

export type RegistrarVendedorProps = { 
  nombre: string
  correo: string
  telefono: string
  direccion: string
  imagen: string
  latitud: string
  longitud: string
 }

@Injectable({
  providedIn: 'root'
})
export class VendedorAddService {

  apiUrl = `http://localhost:5000`

  private http = inject(HttpClient)

  constructor() {

  }

  registrarVendedor(props: RegistrarVendedorProps) {
    return this.http.post<RegistrarVendedorResponse>(`${this.apiUrl}/api/vendedores`, props)
  }

}
