import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { VendedorService } from '../vendedor.service'; // Importa el servicio desde la ruta correcta
import { TranslateModule } from '@ngx-translate/core';

// Interface para los vendedores, si no existe ya en el servicio
interface Vendedor {
  id: string;
  nombre: string;
  correo?: string;
  telefono?: string;
  direccion?: string;
  imagen?: string; // Usaremos esto como la foto
  latitud?: string;
  longitud?: string;
}

@Component({
  selector: 'app-vendedor-list',
  standalone: true,
  imports: [CommonModule, MatButtonModule, TranslateModule],
  templateUrl: './vendedor-list.component.html',
  styleUrls: ['./vendedor-list.component.css']
})
export class VendedorListComponent implements OnInit {
  vendedores: Vendedor[] = [];

  constructor(
    private vendedorService: VendedorService, // Inyecta el servicio
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarVendedores();
  }

  cargarVendedores(): void {
    this.vendedorService.getVendedores().subscribe({
      next: (data) => {
        this.vendedores = data;
        console.log('Vendedores cargados:', this.vendedores);
      },
      error: (err) => {
        console.error('Error al cargar los vendedores:', err);
      }
    });
  }

  verInformes(vendedorId: string): void {
    this.router.navigate(['/ventas/vendedor/informes', vendedorId]);
  }

  verReportes(vendedorId: string): void {
    this.router.navigate(['/ventas/vendedor/reportes', vendedorId]);
  }
}