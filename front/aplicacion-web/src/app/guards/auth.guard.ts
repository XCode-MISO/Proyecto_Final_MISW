import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable, of } from 'rxjs';
import { tap, map, take } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    console.log('AuthGuard: verificando acceso a ruta', state.url);
    
    const isAuth = this.authService.isAuthenticated();
    console.log('¿Usuario autenticado?', isAuth);
    
    if (isAuth) {
      return this.checkRoles(route, state);
    }
    
    // Si no está autenticado, redirigir a login
    this.router.navigate(['/login']);
    return false;
  }
  
  // Verificar roles si es necesario
  private checkRoles(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    const requiredRoles = route.data['roles'] as Array<string>;
    
    if (requiredRoles && requiredRoles.length > 0) {
      const userRole = this.authService.getUserRole();
      console.log('AuthGuard: verificando rol', { requerido: requiredRoles, usuario: userRole });
      
      if (!userRole || !requiredRoles.includes(userRole)) {
        console.log('AuthGuard: rol no autorizado, redirigiendo');
        this.router.navigate(['/access-denied']);
        return false;
      }
    }
    
    console.log('AuthGuard: acceso permitido');
    return true;
  }
}