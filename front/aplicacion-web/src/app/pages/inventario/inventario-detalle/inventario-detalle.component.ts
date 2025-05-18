import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { InventarioListService, DetalleInventarioProducto } from '../inventario-listar/inventario-list.service'; // Ajusta el path si es necesario
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-detalle-producto',
  standalone: true,
  imports: [CommonModule, TranslateModule, FormsModule ],
  templateUrl: './inventario-detalle.component.html',
  styleUrls: ['./inventario-detalle.component.css']
})
export class DetalleProductoComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private inventarioService = inject(InventarioListService);

  producto: DetalleInventarioProducto | null = null;
  error: string | null = null;

  monedaSeleccionada: 'COP' | 'USD' = 'USD';

  precioConvertido: number = 0;

  readonly tasaCambioUSD = 4000;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!isNaN(id)) {
      this.inventarioService.getInventarioId(id).subscribe({
        next: (data) => {
          this.producto = data;
          this.actualizarPrecio();
        },
        error: () => {
          this.error = 'Error al cargar el detalle del producto';
        }
      });
    } else {
      this.error = 'ID inválido';
    }
  }

  actualizarPrecio(): void {
    if (!this.producto) return;

    if (this.monedaSeleccionada === 'COP') {
        this.precioConvertido = this.producto.precio * this.tasaCambioUSD;
    } else {
        this.precioConvertido = this.producto.precio;
    }
}
}
