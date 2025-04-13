import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { ProductosService, FabricanteDto, ProductoDto } from './productos.service';
import { HttpClientModule } from '@angular/common/http';
import { tap } from 'rxjs';

@Component({
  selector: 'app-productos-cargar',
  standalone: true,
  templateUrl: './productos-cargar.component.html',
  styleUrls: ['./productos-cargar.component.css'],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule
  ]
})
export class ProductosCargarComponent implements OnInit {
  private fb = inject(FormBuilder);
  private service = inject(ProductosService);

  form!: FormGroup;
  fabricantes: FabricanteDto[] = [];
  enviado = false;
  mensaje = '';

  ngOnInit(): void {
    this.form = this.fb.group({
      nombre: ['', Validators.required],
      fabricanteId: ['', Validators.required],
      cantidad: [null, [Validators.required, Validators.min(1)]],
      precio: [null, [Validators.required, Validators.min(0.01)]],
      moneda: ['COP', Validators.required],
      bodega: ['', Validators.required],
      estante: ['', Validators.required],
      pasillo: ['', Validators.required],

    });

    this.service.obtenerFabricantes().subscribe((fab) => (this.fabricantes = fab));
  }

  get f() {
    return this.form.controls;
  }

  onSubmit(): void {
    this.enviado = true;
    this.mensaje = '';
    if (this.form.invalid) return;

    const producto: ProductoDto = {
      nombre: this.f['nombre'].value,
      fabricanteId: this.f['fabricanteId'].value,
      cantidad: +this.f['cantidad'].value,
      precio: +this.f['precio'].value,
      moneda: this.f['moneda'].value,
      bodega: this.f['bodega'].value,
      estante: this.f['estante'].value,
      pasillo: this.f['pasillo'].value
    };

    this.service.cargarProducto(producto).pipe(
      tap(() => {
        this.mensaje = 'Producto cargado correctamente';
        this.form.reset();
        this.enviado = false;
      })
    ).subscribe({
      error: () => (this.mensaje = 'Error al cargar el producto')
    });
  }

  onCancel(): void {
    this.form.reset();
    this.enviado = false;
    this.mensaje = '';
  }
}
