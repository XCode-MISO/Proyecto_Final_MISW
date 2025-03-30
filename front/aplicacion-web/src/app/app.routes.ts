import { Routes } from '@angular/router';
import { RoutesComponent } from './routes/routes.component';
import { AppComponent } from './app.component';

export const routes: Routes = [
  { path: '**', component: AppComponent },
  { path: 'routes', component: RoutesComponent }
];
