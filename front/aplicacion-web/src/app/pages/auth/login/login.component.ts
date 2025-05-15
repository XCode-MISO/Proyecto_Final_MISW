import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from '../../../services/auth.service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TranslateModule } from '@ngx-translate/core';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule, 
    ReactiveFormsModule, 
    MatFormFieldModule, 
    MatInputModule, 
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    TranslateModule
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  hidePassword = true;
  errorMessage = '';
  enviado = false;
  mensajeServidor = '';
  isLoading = false;
  returnUrl: string = '/home';
  
  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private authService: AuthService
  ) {
    // Crear formulario
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }
  
  ngOnInit() {
    // Capturar el returnUrl si existe
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/home';
    
    console.log('Login component initialized, returnUrl:', this.returnUrl);
    
    // Verificar si ya está autenticado
    if (this.authService.isAuthenticated()) {
      console.log('Usuario ya autenticado, redirigiendo');
      this.router.navigateByUrl(this.returnUrl);
    }
  }
  
  get f() {
    return this.loginForm.controls;
  }

  onSubmit() {
    this.enviado = true;
    
    if (this.loginForm.invalid) {
      return;
    }
    
    const { email, password } = this.loginForm.value;
    this.isLoading = true;
    
    this.authService.login({ email, password }).subscribe({
      next: (result) => {
        this.isLoading = false;
        if (result.success) {
          console.log('Login exitoso, redirigiendo a:', this.returnUrl);
          this.router.navigateByUrl(this.returnUrl);
        } else {
          this.errorMessage = result.error || 'Error al iniciar sesión';
          this.mensajeServidor = this.errorMessage;
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'Error de conexión. Intente nuevamente.';
        this.mensajeServidor = this.errorMessage;
        console.error('Error de login:', err);
      }
    });
  }
}