import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { VendedorService } from '../vendedor.service';
import { Vendedor } from '../../../routes/routes.component';

interface Reporte {
  id: string;
  fecha: Date;
  producto: string;
  cantidad: number;
}

@Component({
  selector: 'app-vendedor-reportes',
  standalone: true,
  imports: [
    CommonModule,
    TranslateModule,
    MatTableModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './vendedor-reportes.component.html',
  styleUrls: ['./vendedor-reportes.component.css']
})
export class VendedorReportesComponent implements OnInit {
  vendedorId: string = '';
  vendedor: Vendedor | null = null;
  reportes = new MatTableDataSource<Reporte>([]);
  columnas: string[] = ['fecha', 'producto', 'cantidad'];

  constructor(
    private route: ActivatedRoute,
    private vendedorService: VendedorService,
    private snackBar: MatSnackBar,
    private translate: TranslateService
  ) {}

  ngOnInit(): void {
    this.vendedorId = this.route.snapshot.paramMap.get('id') || '';
    this.cargarDatosVendedor();
    this.cargarReportes();
  }

  cargarDatosVendedor(): void {
    if (!this.vendedorId) return;
    
    this.vendedorService.getVendedorPorId(this.vendedorId).subscribe({
      next: (data) => {
        this.vendedor = data;
      },
      error: (error) => {
        this.mostrarError('ERRORS.LOADING_SELLER');
        console.error('Error al cargar datos del vendedor:', error);
      }
    });
  }

  cargarReportes(): void {
    if (!this.vendedorId) return;
    
    this.vendedorService.getReportesPorVendedor(this.vendedorId).subscribe({
      next: (respuesta: any) => {
        console.log('Respuesta completa del servidor:', respuesta);
        
        try {
          // Verificar si la respuesta tiene la estructura esperada
          if (respuesta && typeof respuesta === 'object' && !Array.isArray(respuesta) && 
              respuesta.reportes && Array.isArray(respuesta.reportes)) {
            console.log('Reportes encontrados en objeto:', respuesta.reportes);
            
            // Transformar los datos al formato que espera la tabla
            const reportesTransformados = respuesta.reportes.map((item: any) => ({
              id: item.id?.toString() || String(Math.random()),
              fecha: item.fecha ? new Date(item.fecha) : new Date(),
              producto: item.producto || 'Producto desconocido',
              cantidad: Number(item.cantidad) || 0
            }));
            
            this.reportes.data = reportesTransformados;
            console.log('Datos procesados y asignados a la tabla:', this.reportes.data);
          } else if (Array.isArray(respuesta)) {
            // Si la respuesta es directamente un array
            console.log('La respuesta es un array directo:', respuesta);
            
            const reportesTransformados = respuesta.map((item: any) => ({
              id: item.id?.toString() || String(Math.random()),
              fecha: item.fecha ? new Date(item.fecha) : new Date(),
              producto: item.producto || 'Producto desconocido',
              cantidad: Number(item.cantidad) || 0
            }));
            
            this.reportes.data = reportesTransformados;
            console.log('Datos procesados y asignados a la tabla:', this.reportes.data);
          } else {
            console.error('Formato de respuesta inesperado:', respuesta);
            this.reportes.data = []; // Asignar array vacío en caso de error
          }
        } catch (err) {
          console.error('Error al procesar la respuesta:', err);
          this.reportes.data = []; // Asignar array vacío en caso de error
        }
      },
      error: (error) => {
        this.mostrarError('ERRORS.LOADING_REPORTS');
        console.error('Error al cargar reportes:', error);
        this.reportes.data = []; // Asignar array vacío en caso de error
      }
    });
  }

  private mostrarError(mensaje: string): void {
    this.translate.get(mensaje).subscribe((msg: string) => {
      this.snackBar.open(msg, 'OK', { duration: 5000 });
    });
  }

  mostrarDatosActuales(): void {
    console.log('Estado actual:');
    console.log('Datos en reportes.data:', this.reportes.data);
    console.log('Cantidad de registros:', this.reportes.data.length);
    
    // Mostrar mensaje
    this.snackBar.open(`Hay ${this.reportes.data.length} registros. Revisa la consola para más detalles.`, 'OK', {
      duration: 3000
    });
  }
}