import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { RoutesComponent } from './pages/routes/routes.component';
import { RouteListComponent } from './pages/route-list/route-list.component';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'route/:id', component: RoutesComponent },
  { path: 'route-list', component: RouteListComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full'}
];
