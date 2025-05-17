import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { Router, NavigationEnd, RouterModule } from '@angular/router';
import { filter, takeUntil } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { Subject } from 'rxjs';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';

type Tab = {
  name: string
  route: string
  translationKey: string
}

@Component({
  selector: 'app-navbar',
  imports: [MatButtonModule, MatTabsModule, RouterModule, CommonModule, TranslateModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  standalone: true
})
export class NavbarComponent implements OnInit, OnDestroy {

  private destroy$ = new Subject<void>();
  showNavbar: boolean = false;
  userRole: string | null = null;
  allTabs = [
    { 
      name: "Inicio", 
      route: '/home', 
      roles: ['admin', 'directorcompras', 'directorventas', 'directorlogistica'],
      translationKey: 'NAVIGATION.HOME'
    }, 
    { 
      name: "Gestion de Fabricantes", 
      route: '/fabricantes/menu', 
      roles: ['admin', 'directorcompras'],
      translationKey: 'NAVIGATION.VENDORS'
    }, 
    { 
      name: "Gestion de Ventas", 
      route: '/ventas', 
      roles: ['admin', 'directorventas'],
      translationKey: 'NAVIGATION.SALES'
    }, 
    { //Ruta a menu de gestion de inventario
      name: "Gestion de Inventario", 
      route: '/inventario/menu', 
      roles: ['admin', 'directorlogistica'],
      translationKey: 'NAVIGATION.INVENTORY'
    }
  ];
  
  tabs: { name: string, route: string, translationKey: string }[] = [];
  currentTab: Tab = this.allTabs[0];
  

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  ngOnInit() {
    this.checkRoute(this.router.url);
    
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.checkRoute(event.url);
    });
    
    this.updateTabsByRole();
    
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
          tab.route === '/home' || tab.route === '/fabricantes/menu' || tab.route === '/productos'
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
          tab.route === '/home' || tab.route === '/inventario/menu' || tab.route === '/inventario/route' || tab.route === '/route'||  tab.route === '/inventario/listar' ||  tab.route === '/inventario/detalle'
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

  isPath(tab: any): boolean {
    return this.router.url === tab.route;
  }
  
  navigate(tab: Tab) {
    this.router.navigate([tab.route]);
  }
  filterMenuItemsByRole() {
    if (this.userRole) {
      this.tabs = this.allTabs
        .filter(tab => tab.roles.includes(this.userRole || ''))
        .map(({ name, route, translationKey }) => ({ name, route, translationKey }));
    } else {
      this.tabs = [];
    }
  }
}