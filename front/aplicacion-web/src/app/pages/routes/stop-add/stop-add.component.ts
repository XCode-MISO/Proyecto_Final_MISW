import {ChangeDetectionStrategy, Component, inject, Input, signal} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { Cliente, Route, Vendedor } from '../routes.component';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { catchError, Observable } from 'rxjs';
import { RouteListService } from '../route-list/route-list.service';
import { ActivatedRoute, Router } from '@angular/router';

export type UpdateRoute = Route

@Component({
  selector: 'app-stop-add',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule
  ],
  templateUrl: './stop-add.component.html',
  styleUrl: './stop-add.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StopAddComponent {

  baseRoute?: Route
  @Input()
  route_id?: string

  clientes: Cliente[] = [
    {
      id: "1", 
      nombre: "Cliente1", 
      direccion: "Cra. 11, 82-71, Bogotá, Colombia" 
    },
    {
      id: "2", 
      nombre: "Cliente 2", 
      direccion: "Calle 149, 16-56, Bogotá, Colombia" 
    },
    {
      id: "3", 
      nombre: "Cliente 3", 
      direccion: "Cra. 11, 82-71, Bogotá, Colombia" 
    },
  ]

  vendedores: Vendedor[] =[
    {
      id: "1", 
      nombre: "Vendedor 1", 
      direccion: "Cl. 81 # 13 05, Bogotá" 
    },
    {
      id: "2", 
      nombre: "Vendedor 2", 
      direccion: "Cra. 15 #78-33, Bogotá" 
    },
  ]

  crearParadaForm = new FormGroup({
    vendedor: new FormControl(''),
    cliente: new FormControl(''),
    fecha: new FormControl(''),
    nombre: new FormControl(''),
  });

  router: Router = inject(Router)

  routeService: RouteListService = inject(RouteListService)
  
  constructor(private activatedRoute: ActivatedRoute) {
  }

  ngOnInit(){
    this.route_id = this.activatedRoute.snapshot.paramMap.get("id") || ""
    this.routeService.getRoute(this.route_id).subscribe(this.getRoute.bind(this))
  }

  getRoute(route: Route) {
    this.baseRoute = route
  }

  onSubmit() {
    const formVal = this.crearParadaForm.value
    const fecha = formVal.fecha
    const nombre = formVal.nombre
    const vendedor = this.vendedores.find(c => c.nombre === formVal.vendedor)
    const cliente = this.clientes.find(c => c.nombre === formVal.cliente)

    if (!fecha || !vendedor || !cliente || !nombre) {
      return
    }
    if (!this.baseRoute) {
      console.error("NO BASE ROUTE")
    }
    const route: Route = {...this.baseRoute!!}
    route.paradas.push({
      cliente,
      vendedor,
      fecha,
      nombre
    })
    this.updateRoute(route)
  }

  updateRoute(route: UpdateRoute) {
    this.routeService.updateRoute(route)
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
