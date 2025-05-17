import { Component } from '@angular/core';
import { RouterModule } from '@angular/router'; 
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-gestion-inventario',
  standalone: true,
  imports: [RouterModule, TranslateModule], 
  templateUrl: './gestion-inventario.component.html',
  styleUrl: './gestion-inventario.component.css'
})
export class GestionInventarioComponent {}