import { Component, inject } from '@angular/core';
import { FabricantesListarService, Fabricante } from './fabricantes-listar.service';


@Component({
  selector: 'app-fabricantes-listar',
  imports: [],
  templateUrl: './fabricantes-listar.component.html',
  styleUrl: './fabricantes-listar.component.css'
})
export class FabricantesListarComponent {
  fabricantes: Fabricante[] = [];
  private fabricantesService = inject(FabricantesListarService)
  
  constructor() {
    this.getFabricantes()
  }

  getFabricantes() {
    this.fabricantesService.obtenerFabricantes().subscribe((data) => {
      this.fabricantes = data;
    });
  }
}
