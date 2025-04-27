import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { Router, NavigationEnd, RouterModule } from '@angular/router';
import { filter, takeUntil } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { Subject } from 'rxjs';
import { CommonModule } from '@angular/common';

type Tab = {
  name: string
  route: string
}

@Component({
  selector: 'app-navbar',
  imports: [MatButtonModule, MatTabsModule, RouterModule, CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  standalone: true
})
export class NavbarComponent implements OnInit, OnDestroy {

  private destroy$ = new Subject<void>();
  showNavbar: boolean = false;
  userRole: string | null = null;
  // Definición completa de tabs
  allTabs = [
    { name: "Inicio", route: '/home', roles: ['admin', 'directorcompras', 'directorventas', 'directorlogistica'] }, 
    { name: "Gestion de Fabricantes", route: '/fabricantes/menu', roles: ['admin', 'directorcompras']}, 
    { name: "Gestion de Ventas", route: '/ventas', roles: ['admin', 'directorventas']}, 
    { name: "Gestion de Inventario", route: '/route', roles: ['admin', 'directorlogistica']}
  ];
  
  // Los tabs que se mostrarán según el rol
  tabs: { name: string, route: string }[] = [];
  currentTab: Tab = this.allTabs[0];
  
  // Propiedad para controlar la visibilidad del navbar


  constructor(
    private router: Router,
    private authService: AuthService
  ) {}
  ngOnDestroy(): void {
    // Complete the observable cleanup to prevent memory leaks
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  ngOnInit() {
    // Verificar la ruta inicial
    this.checkRoute(this.router.url);
    
    // Suscribirse a cambios de ruta
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.checkRoute(event.url);
    });
    
    // Actualizar los tabs según el rol del usuario
    this.updateTabsByRole();
    
    // Suscribirse a cambios en la autenticación
    this.authService.userRole$.subscribe(() => {
      this.updateTabsByRole();
    });
  }
  
  // Método para actualizar los tabs según el rol
  updateTabsByRole() {
    const userRole = this.authService.getUserRole();
    
    switch (userRole) {
      case 'admin':
        // Admin puede ver todos los tabs
        this.tabs = [...this.allTabs];
        break;
      case 'directorcompras':
        // DirectorCompras solo puede ver Inicio y Gestión de Fabricantes
        this.tabs = this.allTabs.filter(tab => 
          tab.route === '/home' || tab.route === '/fabricantes/menu'
        );
        break;
      case 'directorventas':
        // DirectorVentas solo puede ver Inicio y Gestión de Ventas
        this.tabs = this.allTabs.filter(tab => 
          tab.route === '/home' || tab.route === '/ventas'
        );
        break;
      case 'directorlogistica':
        // DirectorLogistica solo puede ver Inicio y Gestión de Inventario
        this.tabs = this.allTabs.filter(tab => 
          tab.route === '/home' || tab.route === '/route'
        );
        break;
      default:
        // Si no hay rol o no está autenticado, mostrar solo inicio
        this.tabs = this.allTabs.filter(tab => tab.route === '/home');
        break;
    }
  }
  
  // Método para verificar si debe mostrar la navbar según la ruta
  checkRoute(url: string) {
    // Ocultar en login y en la raíz (que suele redirigir a login)
    const publicRoutes = ['/login', '/', '/access-denied'];
    this.showNavbar = !publicRoutes.includes(url);
    console.log(`NavbarComponent: Ruta actual: ${url}, showNavbar: ${this.showNavbar}`);
  }

  isPath(tab: Tab) {
    const path = this.router.url;
    return path.includes(tab.route);
  }
  
  navigate(tab: Tab) {
    this.router.navigate([tab.route]);
  }
  filterMenuItemsByRole() {
    if (this.userRole) {
      this.tabs = this.allTabs
        .filter(tab => tab.roles.includes(this.userRole || ''))
        .map(({ name, route }) => ({ name, route }));
    } else {
      this.tabs = [];
    }
  }
}