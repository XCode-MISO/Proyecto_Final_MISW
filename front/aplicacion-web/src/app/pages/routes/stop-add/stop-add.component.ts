import { ChangeDetectionStrategy, Component, inject, Input, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { Cliente, Route, Vendedor } from '../routes.component';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { catchError, Observable } from 'rxjs';
import { Parada, RouteListService } from '../route-list/route-list.service';
import { ActivatedRoute, Router } from '@angular/router';
import { VendedorService } from '../../ventas/vendedor/vendedor.service';
import { AsyncPipe } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';

export type UpdateRoute = Route

export type AddStopToRoute = {
  id: string,
  parada: Parada
}

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
    ReactiveFormsModule,
    AsyncPipe,
    TranslateModule
  ],
  templateUrl: './stop-add.component.html',
  styleUrl: './stop-add.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StopAddComponent {

  baseRoute?: Route
  route_id?: string

  clientes?: Observable<Cliente[]>
  clientesDTO?: Cliente[]

  vendedores?: Observable<Vendedor[]>
  vendedoresDTO?: Vendedor[]

  crearParadaForm = new FormGroup({
    vendedor: new FormControl(''),
    cliente: new FormControl(''),
    fecha: new FormControl(''),
    nombre: new FormControl(''),
  });

  router: Router = inject(Router)

  routeService: RouteListService = inject(RouteListService)
  vendedorService: VendedorService = inject(VendedorService)

  constructor(private activatedRoute: ActivatedRoute) {
    this.vendedores = this.getVendedores()
    this.clientes = this.getClientes()
  }

  ngOnInit() {
    this.route_id = this.activatedRoute.snapshot.paramMap.get("id") || ""
    this.routeService.getRoute(this.route_id).subscribe(this.getRoute.bind(this))
  }
  
  getVendedores() {
    const obs = this.vendedorService.getVendedores()
    obs.subscribe((r) => [this.vendedoresDTO = r])
    return obs
  }

  getClientes() {
    const obs = this.vendedorService.getClientes()
    obs.subscribe((r) => [this.clientesDTO = r])
    return obs
  }

  getRoute(route: Route) {
    this.baseRoute = route
  }

  onSubmit() {
    const formVal = this.crearParadaForm.value
    const fecha = formVal.fecha
    const nombre = formVal.nombre
    const vendedor = this.vendedoresDTO!!.find(c => c.id === formVal.vendedor)
    const cliente = this.clientesDTO!!.find(c => c.id === formVal.cliente)

    if (!fecha || !vendedor || !cliente || !nombre) {
      return
    }
    if (!this.baseRoute) {
      console.error("NO BASE ROUTE")
    }
    this.addStopToRoute({
      id: this.route_id!!,
      parada: { cliente, vendedor, nombre, fecha }
    })
  }

  addStopToRoute(route: AddStopToRoute) {
    this.routeService.addStopToRoute(route)
      .pipe(
        catchError((e, source) => {
          console.error(e)
          console.error(source)
          return new Observable()
        })
      )
      .subscribe(result => {
        if (!!(result as { id: string }).id) {
          this.router.navigate([`/route/${(result as { id: string }).id}`])
        }
      })
  }
}
