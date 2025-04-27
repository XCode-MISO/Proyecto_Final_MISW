import { Component } from '@angular/core';
import { ProductosUploadService, ProductosUploadResponse } from './productos-upload.service';
import { Router } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';


@Component({
 
  selector: 'app-Productos-upload',
 
  imports: [CommonModule
    , MatButtonModule],
  
  templateUrl: './Productos-upload.component.html',
  styleUrls: ['./Productos-upload.component.css']
})


export class ProductosUploadComponent {
  isLoading: boolean = false;
  message: string = '';
  errorMessages: string[] = [];
  selectedFile: File | null = null;

  constructor(private uploadService: ProductosUploadService, private router: Router) { }

  irCargaIndividual() {
    this.router.navigate(['/Productos/crear']);
  }

  
  irCargaMasiva() {
    this.router.navigate(['/Productos/upload']);
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file && file.type === 'text/csv') {
      this.selectedFile = file;
    } else {
      this.message = 'Por favor, selecciona un archivo CSV válido.';
      this.selectedFile = null;
    }
  }


  uploadFile() {
    
    if (!this.selectedFile) {
      this.message = 'No hay archivo seleccionado.';
      return;
    }
    this.isLoading = true;
    this.message = '';
    this.errorMessages = [];

    // Crear objeto FormData para enviar
    const formData = new FormData();
    formData.append('file', this.selectedFile, this.selectedFile.name);
    
    this.uploadService.uploadFile(formData).subscribe({
      next: (response: ProductosUploadResponse) => {
        this.isLoading = false;
        if (response.inserted > 0) {
          this.message = `Carga exitosa: ${response.inserted} registros insertados.`;
        }
        if (response.errors && response.errors.length > 0) {
          this.errorMessages = response.errors;
        }
      },
      error: err => {
        this.isLoading = false;
        this.message = 'Error al cargar el archivo.';
      }
    });
  }

  cancelar() {
  
    this.selectedFile = null;
    this.message = '';
    this.errorMessages = [];
    this.isLoading = false;

    this.router.navigate(['/productos/seleccion-carga-producto']);

  }

 
}

