import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap } from 'rxjs/operators';
import { Router } from '@angular/router';
import { from, throwError, of } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  console.log(`📤 Interceptando solicitud a: ${req.url}`, { method: req.method });
  
  // Si la URL es externa, considera usar un proxy o manejarla diferente
if (req.url.includes('microservicios-gateway') && !req.url.includes('ventas_report.cppxcode.shop')) {
    console.warn('⚠️ Detectada petición directa a API Gateway. Considera usar un proxy local.');
  }
  
  
  return from(authService.getToken()).pipe(
    switchMap(token => {
      if (token) {
        req = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`
          }
        });
      }
      
      return next(req).pipe(
        catchError(error => {
          if (error.status === 0) {
            console.error('🔄 Error de conexión: No se pudo conectar con el servidor. Posible problema CORS o de red.');
            // No cerrar sesión en este caso, es un problema de conexión
            return throwError(() => new Error('No se pudo conectar al servidor. Verifica tu conexión o contacta con el administrador.'));
          }
          
          if (error.status === 401) {
            authService.logout();
            router.navigate(['/login']);
          }
          
          return throwError(() => error);
        })
      );
    })
  );
};