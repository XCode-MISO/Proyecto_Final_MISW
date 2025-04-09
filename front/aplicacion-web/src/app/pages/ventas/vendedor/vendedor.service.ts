import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Cliente } from '../../routes/routes.component';

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
export class VendedorService {

  apiUrl = `https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api`

  private http = inject(HttpClient)

  constructor() {

  }

  registrarVendedor(props: RegistrarVendedorProps) {
    return this.http.post<RegistrarVendedorResponse>(`${this.apiUrl}/vendedores`, props)
  }

  getVendedores() {
    return this.http.get<Cliente[]>(`${this.apiUrl}/vendedores`)
  }

  getClientes() {
    return this.http.get<Cliente[]>(`${this.apiUrl}/clients`)
  }

}
