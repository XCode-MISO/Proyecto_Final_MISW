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
import { Auth, sendPasswordResetEmail } from '@angular/fire/auth';
import { MapGeocoder } from '@angular/google-maps';

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
  JSON: any;
  geocoder: MapGeocoder

  constructor(private location: Location, geocoder: MapGeocoder) {
    JSON = JSON
    this.geocoder = geocoder
  }

  crearVendedorForm = new FormGroup({
    nombre: new FormControl('', [Validators.required, Validators.minLength(4)]),
    correo: new FormControl('', [Validators.required, Validators.email]),
    telefono: new FormControl('', [Validators.required, Validators.minLength(7), Validators.maxLength(10)]),
    direccion: new FormControl('', [Validators.required, Validators.minLength(4)]),
  });

  get nombre() {
    return this.crearVendedorForm.get("nombre")
  }
  get correo() {
    return this.crearVendedorForm.get("correo")
  }
  get telefono() {
    return this.crearVendedorForm.get("telefono")
  }
  get direccion() {
    return this.crearVendedorForm.get("direccion")
  }

  registroResponse?: Observable<RegistrarVendedorResponse>

  private vendedorAddService = inject(VendedorService)

  private router: Router = inject(Router)

  private auth = inject(Auth)

  async onSubmit() {

    const formVal = this.crearVendedorForm.value
    const nombre = formVal.nombre
    const correo = formVal.correo
    const telefono = formVal.telefono
    const direccion = formVal.direccion
    if (!correo || !telefono || !direccion || !nombre || !this.crearVendedorForm.valid) {
      return
    }

    const mapsResponse = this.geocoder.geocode({ address: direccion })
    mapsResponse.subscribe(r => {
      const { lat, lng } = r.results?.[0].geometry.location
      this.crearVendedor({
        correo,
        telefono,
        direccion,
        nombre,
        imagen: "https://upload.wikimedia.org/wikipedia/commons/a/a5/Default_Profile_Picture.png",
        latitud: "" + lat(),
        longitud: "" + lng()
      })
    })

  }

  crearVendedor(params: RegistrarVendedorProps) {
    console.log("creando vendedor", params)
    this.registroResponse = this.vendedorAddService.registrarVendedor(params)
    this.registroResponse.subscribe(async (result) => {
      if (result.id) {
        await sendPasswordResetEmail(this.auth, params.correo);
        console.log("vendedor creado:", result)
        this.router.navigate(["/ventas"])
      }
    })
  }

  cancelar() {
    this.location.back()
  }

}
