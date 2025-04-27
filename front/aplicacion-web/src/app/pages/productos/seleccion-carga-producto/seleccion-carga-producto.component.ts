import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-seleccion-carga',
  templateUrl: './seleccion-carga-producto.component.html',
  styleUrls: ['./seleccion-carga-producto.component.css']
})
export class SeleccionCargaProductoComponent {

  constructor(private router: Router) {}

  irCargaIndividual() {
    this.router.navigate(['/productos/crear']);
  }

  irCargaMasiva() {
    this.router.navigate(['/productos/upload']);
  }
}