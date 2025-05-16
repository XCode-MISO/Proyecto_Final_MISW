import { Component } from '@angular/core';
import { RouterModule } from '@angular/router'; 
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-gestion-fabricantes',
  standalone: true,
  imports: [RouterModule, TranslateModule], 
  templateUrl: './gestion-fabricantes.component.html',
  styleUrl: './gestion-fabricantes.component.css'
})
export class GestionFabricantesComponent {}