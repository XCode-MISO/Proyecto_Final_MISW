import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { VendedorService } from '../vendedor.service'; // Importa el servicio desde la ruta correcta
import { TranslateModule } from '@ngx-translate/core';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { TranslateService } from '@ngx-translate/core';
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
  imports: [CommonModule, MatButtonModule, TranslateModule, MatSnackBarModule],
  templateUrl: './vendedor-list.component.html',
  styleUrls: ['./vendedor-list.component.css']
})
export class VendedorListComponent implements OnInit {
  vendedores: any[] = [];

  constructor(
    private vendedorService: VendedorService,    
    private router: Router,
    private snackBar: MatSnackBar,
    private translate: TranslateService
  ) {}

  ngOnInit(): void {
    this.cargarVendedores();
  }

  cargarVendedores(): void {
    this.vendedorService.getVendedores().subscribe({
      next: (data) => {
        this.vendedores = data;
      },
      error: (error) => {
        this.mostrarError('ERRORS.LOADING_SELLERS');
        console.error('Error al cargar vendedores:', error);
      }
    });
  }

  verInformes(vendedorId: string): void {

    //this.router.navigate(['/ventas/vendedor/informes', vendedorId]);
    this.router.navigate(['/ventas/vendedor/informes']);

  }

  verReportes(vendedorId: string): void {
    this.router.navigate(['/ventas/vendedor', vendedorId, 'reportes']);
  }

  private mostrarError(mensaje: string): void {
    this.translate.get(mensaje).subscribe((msg: string) => {
      this.snackBar.open(msg, 'OK', { duration: 5000 });
    });
  }
}