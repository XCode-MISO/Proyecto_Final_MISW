import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import {MatTabsModule} from '@angular/material/tabs';
import { ActivatedRoute, Router } from '@angular/router';

type Tab = {
  name: string
  route: string
}

@Component({
  selector: 'app-navbar',
  imports: [MatButtonModule,MatTabsModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {


  router: Router = inject(Router)

  tabs: Tab[] = [
    { name: "Inicio", 'route': '/home' }, 
    {name: "Gestion de Fabricantes", route: '/fabricantes'}, 
    {name: "Gestion de Ventas", route: '/ventas'}, 
    {name: "Gestion de Inventario", route: '/route'}
  ]
  currentTab: Tab = this.tabs[0]

  constructor(){}

  isPath(tab: Tab) {
    const path = this.router.url

    return path.includes(tab.route)
  }
  navigate(tab:Tab) {
    this.router.navigate([tab.route])
  }
}
