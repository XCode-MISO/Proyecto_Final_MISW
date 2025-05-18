import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { InventarioListService, Inventario } from './inventario-listar/inventario-list.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-producto',
  standalone: true,
  imports: [CommonModule, TranslateModule, FormsModule, MatIconModule],
  templateUrl: './producto.component.html',
  styleUrls: ['./producto.component.css']
})
export class ProductoComponent implements OnInit {
  filtroNombre: string = '';
  productosOriginales: Inventario[] = [];
  productosFiltrados: Inventario[] = [];

  private router = inject(Router);
  private inventarioListService = inject(InventarioListService);

  ngOnInit(): void {
    this.inventarioListService.getInventario().subscribe((productos) => {
      this.productosOriginales = productos;
      this.actualizarFiltro();
    });
  }

  actualizarFiltro(): void {
    const filtro = this.filtroNombre.toLowerCase();
    this.productosFiltrados = this.productosOriginales.filter(producto =>
      producto.nombre.toLowerCase().includes(filtro)
    );
  }

  navigateToDetalle(producto_id: number): void {
    this.router.navigate(['/inventario/detalle/', producto_id]);
  }

  trackByProductoId(index: number, producto: any): any {
    return producto.producto_id;
  }
}
