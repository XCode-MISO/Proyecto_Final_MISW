import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-seleccion-carga',
  templateUrl: './seleccion-carga.component.html',
  styleUrls: ['./seleccion-carga.component.css'],
   imports: [
    TranslateModule
  ]
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