import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';

export interface ProductosUploadResponse {
  inserted: number;
  errors: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ProductosUploadService {

  private readonly uploadUrl = `${environment.apiUrl}/api/productos/upload`

  constructor(private http: HttpClient) { }

  /**
   * Envía al backend el archivo CSV para la carga masiva de Productos.
   * @param formData Objeto FormData que contiene el archivo CSV.
   */
  uploadFile(formData: FormData): Observable<ProductosUploadResponse> {
    return this.http.post<ProductosUploadResponse>(this.uploadUrl, formData)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Manejo básico de errores HTTP
   */
  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Ocurrió un error desconocido.';
    if (error.error instanceof ErrorEvent) {
      // Error del cliente o red
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Error retornado por el backend
      errorMessage = `Código de error: ${error.status}\nMensaje: ${error.message}`;
    }
    return throwError(() => errorMessage);
  }
}


