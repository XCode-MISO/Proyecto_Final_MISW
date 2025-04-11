import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { RegistrarVendedorProps, RegistrarVendedorResponse, VendedorService } from '../vendedor.service';
import { Observable } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-vendedor-add',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatDatepickerModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    AsyncPipe
  ],
  templateUrl: './vendedor-add.component.html',
  styleUrl: './vendedor-add.component.css'
})
export class VendedorAddComponent {

  constructor(private location: Location) {

  }

  crearVendedorForm = new FormGroup({
    nombre: new FormControl('', [Validators.required, Validators.minLength(4)]),
    correo: new FormControl('', [Validators.required, Validators.email]),
    telefono: new FormControl('', [Validators.required, Validators.minLength(8), Validators.maxLength(8)]),
    direccion: new FormControl('', [Validators.required, Validators.minLength(4)]),
  });

  get nombre(){
    return this.crearVendedorForm.get("nombre")
  }
  get correo(){
    return this.crearVendedorForm.get("correo")
  }
  get telefono(){
    return this.crearVendedorForm.get("telefono")
  }
  get direccion(){
    return this.crearVendedorForm.get("direccion")
  }

  registroResponse?: Observable<RegistrarVendedorResponse>
  
  private vendedorAddService = inject(VendedorService)

  private router: Router = inject(Router)

  onSubmit() {
    
    const formVal = this.crearVendedorForm.value
    const nombre = formVal.nombre
    const correo = formVal.correo
    const telefono = formVal.telefono
    const direccion = formVal.direccion
    if (!correo || !telefono || !direccion || !nombre) {
      return
    }
    this.crearVendedor({
      correo,
      telefono,
      direccion,
      nombre,
      imagen: "https://upload.wikimedia.org/wikipedia/commons/a/a5/Default_Profile_Picture.png",
      latitud: "45",
      longitud: "45"
    })
  }
  crearVendedor(params: RegistrarVendedorProps) {
    this.registroResponse = this.vendedorAddService.registrarVendedor(params)
    this.registroResponse.subscribe((result) => {
      if (result.id){
        this.router.navigate(["/ventas"])
      }
    })
  }

  cancelar() {
    this.location.back()
  }

}
