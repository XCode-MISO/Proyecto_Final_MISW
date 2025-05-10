import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { RoutesComponent } from './pages/routes/routes.component';
import { RouteListComponent } from './pages/routes/route-list/route-list.component';
import { StopAddComponent } from './pages/routes/stop-add/stop-add.component';
import { RouteAddComponent } from './pages/routes/route-add/route-add.component';
import { FabricantesListarComponent } from './pages/fabricantes/fabricantes-listar/fabricantes-listar.component';
import { FabricantesCrearComponent } from './pages/fabricantes/fabricantes-crear/fabricantes-crear.component';
import { ProductosCargarComponent } from './pages/productos/productos-cargar/productos-cargar.component';
import { GestionFabricantesComponent } from './pages/fabricantes/gestion-fabricantes/gestion-fabricantes.component';
import { SeleccionCargaComponent } from './pages/fabricantes/seleccion-carga/seleccion-carga.component';
import { SeleccionCargaProductoComponent } from './pages/productos/seleccion-carga-producto/seleccion-carga-producto.component';
import { FabricantesUploadComponent } from './pages/fabricantes/fabricantes-upload/fabricantes-upload.component';
import { ProductosUploadComponent } from './pages/productos/productos-upload/productos-upload.component';
import { MenuComponent } from './pages/ventas/menu/menu.component';
import { VendedorAddComponent } from './pages/ventas/vendedor/vendedor-add/vendedor-add.component';
import { LoginComponent } from './pages/auth/login/login.component';
import { AuthGuard } from './guards/auth.guard';
import { AccessDeniedComponent } from './pages/errors/access-denied/access-denied.component';
import { PlansComponent } from './pages/plans/plans.component';
import { AddPlanComponent } from './pages/plans/add-plan/add-plan.component';

export const routes: Routes = [
  // Rutas públicas
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'access-denied', component: AccessDeniedComponent },
  
  // Home - Accesible para todos los usuarios autenticados
  { 
    path: 'home', 
    component: HomeComponent,
    canActivate: [AuthGuard]
  },
  
  // Rutas de Fabricantes - Solo para admin y directorcompras
  { 
    path: 'fabricantes', 
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'directorcompras'] },
    children: [
      { path: 'listar', component: FabricantesListarComponent },
      { path: 'crear', component: FabricantesCrearComponent },
      { path: 'menu', component: GestionFabricantesComponent },
      { path: 'seleccion-carga', component: SeleccionCargaComponent },
      { path: 'upload', component: FabricantesUploadComponent },
    ]
  },
  
  // Rutas de Productos - Solo para admin y directorcompras
  { 
    path: 'fabricantes', 
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'directorcompras'] },
    children: [
      { path: 'crear-producto', component: ProductosCargarComponent },
      { path: 'seleccion-carga-productos', component: SeleccionCargaProductoComponent },
      { path: 'upload-productos', component: ProductosUploadComponent },
    ]
  },
  
  // Rutas de Ventas - Solo para admin y directorventas
  { 
    path: 'ventas', 
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'directorventas'] },
    children: [
      { path: '', component: MenuComponent },
      { path: 'vendedor/add', component: VendedorAddComponent },
    ]
  },
  {
    path: 'plan/add',
    component: AddPlanComponent,
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'directorventas'] }
  },
  
  // Rutas de Inventario/Logística - Solo para admin y directorlogistica
  { 
    path: 'route', 
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'directorlogistica'] },
    children: [
      { path: '', component: RouteListComponent },
      { path: 'add', component: RouteAddComponent },
      { path: ':id', component: RoutesComponent },
      { path: ':id/stop/add', component: StopAddComponent },
      { path: ':id/stop/:id', component: StopAddComponent },
    ]
  },
  { 
    path: 'route-add', 
    component: RouteAddComponent,
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'directorlogistica'] }
  },
  
  // Ruta de redirección para rutas no encontradas
  { path: '**', redirectTo: '/login' }
];