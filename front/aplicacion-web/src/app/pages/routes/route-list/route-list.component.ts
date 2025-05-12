import { Component, inject, input } from '@angular/core';
import { RouteListService } from './route-list.service';
import { Route } from '../routes.component';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';          
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-route-list',
  imports: [
    MatButtonModule, 
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatDatepickerModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    TranslateModule
  ],
  templateUrl: './route-list.component.html',
  styleUrl: './route-list.component.css'
})
export class RouteListComponent {

  dateFilter = new FormControl('')

  navigateToRouteAdd() {
    this.router.navigate(['route-add'])
  }

  router: Router = inject(Router)

  routes: Route[] = []
  filteredRoutes: Route[] = this.routes

  private routesListService = inject(RouteListService)

  constructor() {
    this.getRoutes()
  }

  getRoutes() {
    this.routes = []
    this.routesListService.getRoutes().subscribe((routes) => {
      this.routes = routes
      this.filterRoutes()
    })
  }

  navigateToRoute(id: string) {
    console.log(this.routes)
    this.router.navigate([`/route/${id}`])
  }

  filterRoutes(){
    this.filteredRoutes = this.routes.filter(r => {
      if (!this.dateFilter.value) return true

      const routeDate = new Date(r.fecha)
      const routeDateDay = new Date(routeDate.getFullYear(),routeDate.getMonth(),routeDate.getDay())

      const dateFilter = new Date(this.dateFilter.value)
      const filterDay = new Date(dateFilter.getFullYear(),dateFilter.getMonth(),dateFilter.getDay())

      return routeDateDay == filterDay
    })
  }
}
