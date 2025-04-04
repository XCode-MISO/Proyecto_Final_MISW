import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { Route } from '../routes.component';
import { Parada, RouteListService } from '../route-list/route-list.service';
import { Router } from '@angular/router';
import { catchError, Observable } from 'rxjs';

export type CreateRoute = {
  nombre: string
  fecha: string
  inicio: string
  fin: string
  paradas: Parada[]
}

@Component({
  selector: 'app-route-add',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatDatepickerModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule
  ],
  templateUrl: './route-add.component.html',
  styleUrl: './route-add.component.css'
})
export class RouteAddComponent {
  crearRutaForm = new FormGroup({
    nombre: new FormControl(''),
    inicio: new FormControl(''),
    fin: new FormControl(''),
    fecha: new FormControl(''),
  });

  router: Router = inject(Router)

  routeService: RouteListService = inject(RouteListService)

  onSubmit() {
    const formVal = this.crearRutaForm.value
    const fecha = formVal.fecha
    const inicio = formVal.inicio
    const fin = formVal.fin
    const nombre = formVal.nombre
    if (!fecha || !inicio || !fin || !nombre) {
      return
    }
    this.crearRuta({
      fecha,
      inicio,
      fin,
      nombre,
      paradas: []
    })
  }

  crearRuta(route: CreateRoute) {
    this.routeService.generateRoute(route)
      .pipe(
        catchError((e, source) => {
          console.error(e)
          console.error(source)
          return new Observable()
        })
      )
      .subscribe(result => {
        if (!!(result as {route_id:string}).route_id) {
          this.router.navigate([`/route/${(result as {route_id:string}).route_id}`])
        }
      })
  }
}
