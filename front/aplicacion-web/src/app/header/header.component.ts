import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NavbarComponent } from "../navbar/navbar.component";
import { LOCALE_ID, Inject, ɵsetLocaleId } from '@angular/core';
import { MatMenuModule } from '@angular/material/menu';
import { AuthService } from '../services/auth.service';
import { Subject } from 'rxjs';
import { Router, NavigationEnd } from '@angular/router';
import { filter, takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-header',
  imports: [MatToolbarModule, MatButtonModule, MatIconModule, NavbarComponent, MatMenuModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
  standalone: true
})
export class HeaderComponent implements OnInit, OnDestroy {
  selectedLocale: string;
  availableLocales: string[] = ["es", "en-US"];
  isLoginPage: boolean = false;
  private destroy$ = new Subject<void>();

  constructor(
    @Inject(LOCALE_ID) public locale: string,
    private authService: AuthService,
    private router: Router
  ) { 
    this.selectedLocale = locale;
  }

  ngOnInit() {
    // Verificar la ruta inicial
    this.checkIsLoginPage(this.router.url);
    
    // Suscribirse a cambios de ruta
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd),
      takeUntil(this.destroy$)
    ).subscribe((event: any) => {
      this.checkIsLoginPage(event.url);
    });
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private checkIsLoginPage(url: string) {
    const publicRoutes = ['/login', '/', '/access-denied'];
    this.isLoginPage = publicRoutes.includes(url);
    console.log(`HeaderComponent: URL=${url}, isLoginPage=${this.isLoginPage}`);
  }

  setLocale(localeId: string) {
    ɵsetLocaleId(localeId);
  }

  onLogout() {
    this.authService.logout().subscribe({
      next: () => {
        console.log('Sesión cerrada correctamente');
        // El servicio de autenticación ya se encargará de la redirección
      },
      error: (err) => {
        console.error('Error al cerrar sesión:', err);
      }
    });
  }
}