import { Component, inject } from '@angular/core';
import { RouteListService } from './route-list.service';
import { Route } from '../routes/routes.component';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-route-list',
  imports: [MatButtonModule],
  templateUrl: './route-list.component.html',
  styleUrl: './route-list.component.css'
})
export class RouteListComponent {

  router: Router = inject(Router)

  routes: Route[] = []
  private routesListService = inject(RouteListService)

  constructor() {
    this.getRoutes()
  }

  getRoutes() {
    this.routes = []
    this.routesListService.getRoutes().subscribe((routes) => (this.routes = routes))
  }

  navigateToRoute(id: string) {
    console.log(this.routes)
    this.router.navigate([`/route/${id}`])
  }
}
