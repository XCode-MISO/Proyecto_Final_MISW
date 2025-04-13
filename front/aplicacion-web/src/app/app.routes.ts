import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { RoutesComponent } from './pages/routes/routes.component';
import { RouteListComponent } from './pages/routes/route-list/route-list.component';
import { StopAddComponent } from './pages/routes/stop-add/stop-add.component';
import { RouteAddComponent } from './pages/routes/route-add/route-add.component';
import { FabricantesListarComponent } from './pages/fabricantes/fabricantes-listar/fabricantes-listar.component'
import { FabricantesCrearComponent } from './pages/fabricantes/fabricantes-crear/fabricantes-crear.component'
import { ProductosCargarComponent } from './pages/productos/productos-cargar/productos-cargar.component';
import { GestionFabricantesComponent } from './pages/fabricantes/gestion-fabricantes/gestion-fabricantes.component';
import { SeleccionCargaComponent } from './pages/fabricantes/seleccion-carga/seleccion-carga.component';
import { FabricantesUploadComponent } from './pages/fabricantes/fabricantes-upload/fabricantes-upload.component';
export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  {
    path: 'route', 
    component: RouteListComponent,
    children: [
      { path: 'add', component: RouteAddComponent }
    ]
  },
  {
    path: 'route/:id',
    component: RoutesComponent,
  },
  {
    path: 'route/:id/stop/add', component: StopAddComponent
  },
  {
    path: 'route/:id/stop/:id', component: StopAddComponent
  },
  { path: 'route-add', component: RouteAddComponent },
  { path: 'fabricantes/listar',component: FabricantesListarComponent },
  { path: 'fabricantes/crear',component: FabricantesCrearComponent },
  { path: 'fabricantes/menu',component: GestionFabricantesComponent },
  { path: 'productos/crear',component: ProductosCargarComponent },
  { path: 'fabricantes/seleccion-carga', component: SeleccionCargaComponent },
  { path: 'fabricantes/upload',component: FabricantesUploadComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }
];
