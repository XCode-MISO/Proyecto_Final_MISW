import { Routes } from '@angular/router';
import { RoutesComponent } from './routes/routes.component';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'routes', component: RoutesComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full'}
];
