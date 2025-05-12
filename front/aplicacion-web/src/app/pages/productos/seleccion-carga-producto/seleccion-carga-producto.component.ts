import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-seleccion-carga',
  templateUrl: './seleccion-carga-producto.component.html',
  styleUrls: ['./seleccion-carga-producto.component.css'],
  imports: [TranslateModule]
})
export class SeleccionCargaProductoComponent {

  constructor(private router: Router) {}

  irCargaIndividual() {
    this.router.navigate(['/fabricantes/crear-producto']);
  }

  irCargaMasiva() {
    this.router.navigate(['/fabricantes/upload-productos']);
  }
}