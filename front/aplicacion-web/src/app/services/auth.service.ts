import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, from, of } from 'rxjs';
import { catchError, map, switchMap, tap } from 'rxjs/operators';
import { Auth, onAuthStateChanged, signInWithEmailAndPassword, signOut, setPersistence, browserLocalPersistence, getIdTokenResult } from '@angular/fire/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();
  
  private userRoleSubject = new BehaviorSubject<string | null>(null);
  public userRole$ = this.userRoleSubject.asObservable();

  constructor(
    private auth: Auth,
    private router: Router
  ) {
    console.log('AuthService: Inicializando...');
    
    // Establecer persistencia para mantener sesión
  
    
    // Observable para estado de autenticación
    onAuthStateChanged(this.auth, async (user) => {
      console.log('Estado de autenticación cambió:', user ? `Usuario ${user.email}` : 'No hay usuario');
      
      if (user) {
        // Usuario autenticado
        this.isAuthenticatedSubject.next(true);
        
        try {
          // Obtener rol desde token
          const tokenResult = await user.getIdTokenResult(true);
          const role = tokenResult.claims["role"] as string | null;
          console.log('Rol del usuario:', role);
          this.userRoleSubject.next(role);
          
          // Guardar últimos datos conocidos en localStorage como respaldo
          localStorage.setItem('authUser', JSON.stringify({
            uid: user.uid,
            email: user.email,
            role: role
          }));
        } catch (error) {
          console.error('Error obteniendo token:', error);
        }
      } else {
        // Usuario no autenticado
        this.isAuthenticatedSubject.next(false);
        this.userRoleSubject.next(null);
        localStorage.removeItem('authUser');
      }
    });
  }

  // Verificar autenticación de manera síncrona
  isAuthenticated(): boolean {
    // Verificar Firebase Auth directamente
    const currentUser = this.auth.currentUser;
    
    // Si tenemos usuario actual, estamos autenticados
    if (currentUser) {
      console.log('isAuthenticated: Usuario encontrado en Firebase Auth');
      return true;
    }
    
    // Si no hay usuario pero tenemos datos guardados, consideramos autenticado
    const authUserStr = localStorage.getItem('authUser');
    if (authUserStr) {
      console.log('isAuthenticated: Usuario encontrado en localStorage');
      return true;
    }
    
    // No tenemos información de autenticación
    console.log('isAuthenticated: No hay usuario autenticado');
    return false;
  }

  // Obtener rol de usuario
  getUserRole(): string | null {
    // Si tenemos el valor en el subject, usarlo
    const roleFromSubject = this.userRoleSubject.value;
    if (roleFromSubject) {
      return roleFromSubject;
    }
    
    // Si no, intentar obtenerlo desde localStorage
    try {
      const authUserStr = localStorage.getItem('authUser');
      if (authUserStr) {
        const authUser = JSON.parse(authUserStr);
        return authUser.role || null;
      }
    } catch (e) {
      console.error('Error al leer rol desde localStorage:', e);
    }
    
    return null;
  }

  // Login con Firebase
  login(credentials: { email: string; password: string }): Observable<any> {
    console.log('Intentando login con:', credentials.email);
    
    return from(signInWithEmailAndPassword(
      this.auth,
      credentials.email,
      credentials.password
    )).pipe(
      switchMap(userCredential => {
        console.log('Login exitoso');
        
        return from(userCredential.user.getIdTokenResult()).pipe(
          map(tokenResult => {
            const role = tokenResult.claims["role"];
            console.log('Rol obtenido del token:', role);
            
            // No necesitamos guardar esto manualmente, el listener de onAuthStateChanged lo hará
            
            return {
              success: true,
              user: {
                uid: userCredential.user.uid,
                email: userCredential.user.email,
                role: role
              }
            };
          })
        );
      }),
      catchError(error => {
        console.error('Error en login:', error);
        let errorMessage = 'Error al iniciar sesión';
        
        switch(error.code) {
          case 'auth/invalid-credential':
          case 'auth/user-not-found':
          case 'auth/wrong-password':
            errorMessage = 'Email o contraseña incorrectos';
            break;
          case 'auth/too-many-requests':
            errorMessage = 'Demasiados intentos fallidos. Intenta más tarde';
            break;
          default:
            errorMessage = `Error: ${error.message}`;
        }
        
        return of({
          success: false,
          error: errorMessage
        });
      })
    );
  }

  // Cerrar sesión
  logout(): Observable<boolean> {
    return from(signOut(this.auth)).pipe(
      tap(() => {
        // Ya no necesitamos limpiar localStorage manualmente
        // El listener de onAuthStateChanged lo hará
        this.router.navigate(['/login']);
      }),
      map(() => true),
      catchError(error => {
        console.error('Error al cerrar sesión:', error);
        return of(false);
      })
    );
  }

  // Método auxiliar para depuración y diagnóstico
  async diagnosticInfo(): Promise<any> {
    const currentUser = this.auth.currentUser;
    let tokenInfo = null;
    
    if (currentUser) {
      try {
        const token = await currentUser.getIdTokenResult();
        tokenInfo = {
          hasToken: true,
          expirationTime: token.expirationTime,
          role: token.claims["role"]
        };
      } catch (e) {
        tokenInfo = { error: e };
      }
    }
    
    return {
      currentUser: currentUser ? {
        uid: currentUser.uid,
        email: currentUser.email,
      } : null,
      tokenInfo,
      isAuthenticatedSubject: this.isAuthenticatedSubject.value,
      userRoleSubject: this.userRoleSubject.value,
      localStorageUser: localStorage.getItem('authUser')
    };
  }

  async getToken(): Promise<string | null> {
    try {
      const user = this.auth.currentUser;
      if (!user) {
        console.log('getToken: No hay usuario autenticado');
        return null;
      }
      
      // Obtener token fresco de Firebase
      const token = await user.getIdToken(true);
      console.log('getToken: Token obtenido con éxito',token);
      return token;
    } catch (error) {
      console.error('Error al obtener token:', error);
      return null;
    }
  }

}