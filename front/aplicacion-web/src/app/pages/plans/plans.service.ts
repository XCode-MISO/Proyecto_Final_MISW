import { inject, Injectable } from '@angular/core';
import { RegistrarVendedorProps } from '../ventas/vendedor/vendedor.service';
import { HttpClient } from '@angular/common/http';
import { Vendedor } from '../routes/routes.component';

export type RegistrarPlanResponse = {
  id: string;
  createdAt: string;
};

export type RegistrarPlanProps = {
  fecha: string;
  descripcion: string;
  vendedores: Vendedor[];
};

export type Plan = {
  id: string;
  fecha: string;
  descripcion: string;
  vendedores: RegistrarVendedorProps[];
};

@Injectable({
  providedIn: 'root',
})
export class PlansService {
  apiUrl = `https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api`;

  private http = inject(HttpClient);

  constructor() {}

  registrarPlan(props: RegistrarPlanProps) {
    return this.http.post<RegistrarPlanResponse>(`${this.apiUrl}/plan`, props);
  }

  getPlanes() {
    return this.http.get<Plan[]>(`${this.apiUrl}/plan`);
  }
}
