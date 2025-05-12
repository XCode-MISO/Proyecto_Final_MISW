import { Component } from '@angular/core';
import { FabricantesUploadService, FabricantesUploadResponse } from './fabricantes-upload.service';
import { Router } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { TranslateModule } from '@ngx-translate/core';


@Component({
 
  selector: 'app-fabricantes-upload',
 
  imports: [CommonModule
    , MatButtonModule, TranslateModule],
  
  templateUrl: './fabricantes-upload.component.html',
  styleUrls: ['./fabricantes-upload.component.css']
})


export class FabricantesUploadComponent {
  isLoading: boolean = false;
  message: string = '';
  errorMessages: string[] = [];
  selectedFile: File | null = null;

  constructor(private uploadService: FabricantesUploadService, private router: Router) { }

  irCargaIndividual() {
    this.router.navigate(['/fabricantes/crear']);
  }

  
  irCargaMasiva() {
    this.router.navigate(['/fabricantes/upload']);
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
      next: (response: FabricantesUploadResponse) => {
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

    this.router.navigate(['/fabricantes/seleccion-carga']);

  }

 
}

