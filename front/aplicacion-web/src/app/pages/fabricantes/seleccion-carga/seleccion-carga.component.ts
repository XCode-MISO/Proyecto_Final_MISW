import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-seleccion-carga',
  templateUrl: './seleccion-carga.component.html',
  styleUrls: ['./seleccion-carga.component.css']
})
export class SeleccionCargaComponent {

  constructor(private router: Router) {}

  irCargaIndividual() {
    this.router.navigate(['/fabricantes/crear']);
  }

  irCargaMasiva() {
    this.router.navigate(['/fabricantes/upload']);
  }
}