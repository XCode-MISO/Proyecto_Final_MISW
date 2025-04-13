import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FabricantesCrearService } from './fabricantes-crear.service';
import { CommonModule, NgIf } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';




export interface Fabricante {
  nombre: string;
  correo: string;
  telefono: string;
  empresa: string;
}

@Component({
  selector: 'app-fabricantes-crear',
  templateUrl: './fabricantes-crear.component.html',
  styleUrls: ['./fabricantes-crear.component.css'],
  imports: [
    CommonModule,          
    ReactiveFormsModule,   
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    HttpClientModule
  ]
})
export class FabricantesCrearComponent implements OnInit {
  fabricanteForm!: FormGroup;
  enviado = false;
  mensajeServidor = '';

  constructor(
    private fb: FormBuilder,
    private fabricanteService: FabricantesCrearService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.fabricanteForm = this.fb.group({
      nombre: [
        '',
        [Validators.required, Validators.maxLength(150)]
      ],
      correo: [
        '',
        [Validators.required, Validators.email]
      ],
      telefono: [
        '',
        [
          Validators.required,
          Validators.pattern('^\\d{7,15}$')
        ]
      ],
      empresa: [
        '',
        [Validators.required, Validators.maxLength(150)]
      ]
    });
  }

  // Accesores para fácil acceso en la plantilla
  get f() {
    return this.fabricanteForm.controls;
  }

  onSubmit(): void {
    this.enviado = true;
    this.mensajeServidor = '';

    if (this.fabricanteForm.invalid) {
      return;
    }

    const nuevoFabricante: Fabricante = this.fabricanteForm.value;

    this.fabricanteService.crearFabricante(nuevoFabricante).subscribe({
      next: () => {
        this.mensajeServidor = 'Fabricante registrado correctamente';
        this.fabricanteForm.reset();
        this.enviado = false;
      },
      error: (err) => {
        console.error(err);
        this.mensajeServidor = 'Ocurrió un error al registrar el fabricante';
      }
    });
  }

  onCancel(): void {
    this.fabricanteForm.reset();
    this.enviado = false;
    this.mensajeServidor = '';
    this.router.navigate(['/fabricantes/seleccion-carga']);
  }
}