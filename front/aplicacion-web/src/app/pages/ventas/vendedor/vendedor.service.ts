import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Cliente, Vendedor } from '../../routes/routes.component';
import { VendedorVisita } from './vendedor-visit-list/vendedor-visit-list.component';

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

  reportesUrl = 'http://ventas_report.cppxcode.shop/api'

  private http = inject(HttpClient)

  constructor() {

  }

  registrarVendedor(props: RegistrarVendedorProps) {
    return this.http.post<RegistrarVendedorResponse>(`${this.apiUrl}/vendedores`, props)
  }

  getVendedores() {
    return this.http.get<Vendedor[]>(`${this.apiUrl}/vendedores`)
  }

  getClientes() {
    return this.http.get<Cliente[]>(`${this.apiUrl}/clients`)
  }


  getVendedorPorId(id: string) {
    return this.http.get<Vendedor>(`${this.apiUrl}/vendedores/${id}`)
  }
  
  getReportesPorVendedor(vendedorId: string) {
      return this.http.get<any[]>(`${this.reportesUrl}/reportes/vendedor/${vendedorId}`);
 }


  getVisitas() {
    return this.http.get<VendedorVisita[]>(`${this.apiUrl}/visits`);
  }

}

