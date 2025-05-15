import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NavbarComponent } from "../navbar/navbar.component";
import { LOCALE_ID, Inject } from '@angular/core';
import { MatMenuModule } from '@angular/material/menu';
import { AuthService } from '../services/auth.service';
import { Subject } from 'rxjs';
import { Router, NavigationEnd } from '@angular/router';
import { filter, takeUntil } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { TranslateService, TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-header',
  imports: [
    MatToolbarModule, 
    MatButtonModule, 
    MatIconModule, 
    NavbarComponent, 
    MatMenuModule, 
    CommonModule,
    TranslateModule 
  ],
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
    public authService: AuthService,
    private router: Router,
    private translate: TranslateService 
  ) { 
    
    this.selectedLocale = localStorage.getItem('userLocale') || locale;
    

    this.translate.addLangs(this.availableLocales);
    this.translate.setDefaultLang('es');
    
   
    this.translate.use(this.selectedLocale);
  }

  ngOnInit() {
    
    this.checkIsLoginPage(this.router.url);
   
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
  }

  setLocale(localeId: string) {
    
    this.selectedLocale = localeId;
    
    localStorage.setItem('userLocale', localeId);
    
    this.translate.use(localeId);
  }

  onLogout() {
    this.authService.logout().subscribe({
      next: () => {
        console.log('Sesión cerrada correctamente');
      },
      error: (err) => {
        console.error('Error al cerrar sesión:', err);
      }
    });
  }
}