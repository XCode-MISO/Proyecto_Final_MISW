import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap } from 'rxjs/operators';
import { Router } from '@angular/router';
import { from, throwError, of } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  return from(authService.getToken()).pipe(
    switchMap(token => {
      // Solo añadir token si existe
      if (token) {
        req = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`
          }
        });
      }
      
      return next(req).pipe(
        catchError(error => {
          // Si es error de autenticación (401), cerrar sesión
          if (error.status === 401) {
            authService.logout();
          }
          return throwError(() => error);
        })
      );
    })
  );
};