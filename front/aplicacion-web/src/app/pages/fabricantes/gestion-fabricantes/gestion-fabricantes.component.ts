import { Component } from '@angular/core';
import { RouterModule } from '@angular/router'; // 👈 este import es clave

@Component({
  selector: 'app-gestion-fabricantes',
  standalone: true,
  imports: [RouterModule], 
  templateUrl: './gestion-fabricantes.component.html',
  styleUrl: './gestion-fabricantes.component.css'
})
export class GestionFabricantesComponent {}