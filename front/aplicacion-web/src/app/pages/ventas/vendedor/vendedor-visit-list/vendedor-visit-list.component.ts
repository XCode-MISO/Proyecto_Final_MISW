import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { VendedorService } from '../vendedor.service'; // Importa el servicio desde la ruta correcta
import { TranslateModule } from '@ngx-translate/core';

// Interface para los visitas, si no existe ya en el servicio
export interface VendedorVisita {
  id: string;
  fechaVisita: string;
  informe: string;
}

@Component({
  selector: 'app-vendedor-list',
  standalone: true,
  imports: [CommonModule, MatButtonModule, TranslateModule],
  templateUrl: './vendedor-visit-list.component.html',
  styleUrls: ['./vendedor-visit-list.component.css']
})
export class VendedorVisitListComponent implements OnInit {
  visitas: VendedorVisita[] = [];

  constructor(
    private vendedorService: VendedorService, // Inyecta el servicio
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarVendedores();
  }

  cargarVendedores(): void {
    this.vendedorService.getVisitas().subscribe({
      next: (data) => {
        this.visitas = data;
      },
      error: (err) => {
        console.error('Error al cargar visitas:', err);
      }
    });
  }
}