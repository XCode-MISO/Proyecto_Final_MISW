import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';

type Tab = {
  name: string
  route: string
}

@Component({
  selector: 'app-navbar',
  imports: [MatButtonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  tabs: Tab[] = [{ name: "Inicio", 'route': '' }, {name: "Gestion de Fabricantes", route: '/'}, {name: "Gestion de Ventas", route: ''}, {name: "Gestion de Inventario", route: ''}]
}
