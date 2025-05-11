import { Component, inject } from '@angular/core';
import { RouteListService } from '../../routes/route-list/route-list.service';
import {
  FormGroup,
  FormControl,
  Validators,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { Observable } from 'rxjs';
import {
  PlansService,
  RegistrarPlanProps,
  RegistrarPlanResponse,
} from '../plans.service';
import { VendedorService } from '../../ventas/vendedor/vendedor.service';
import { Vendedor } from '../../routes/routes.component';
import { Router } from '@angular/router';
import { AsyncPipe } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-add-plan',
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
    AsyncPipe,
  ],
  templateUrl: './add-plan.component.html',
  styleUrl: './add-plan.component.css',
})
export class AddPlanComponent {
  vendedores: Observable<Vendedor[]>;
  vendedoresDto!: Vendedor[];
  vendedoreService: VendedorService = inject(VendedorService);
  planService: PlansService = inject(PlansService);

  constructor(private router: Router) {
    this.vendedores = this.getVendedores();
  }
  getVendedores() {
    const obs = this.vendedoreService.getVendedores();
    obs.subscribe((r) => [(this.vendedoresDto = r)]);
    return obs;
  }

  routeService: RouteListService = inject(RouteListService);

  crearPlanForm = new FormGroup({
    fecha: new FormControl('', [Validators.required]),
    descripcion: new FormControl('', [Validators.required]),
    vendedores: new FormControl('', [Validators.required]),
  });

  get fecha() {
    return this.crearPlanForm.get('fecha');
  }
  get descripcion() {
    return this.crearPlanForm.get('descripcion');
  }

  registroResponse?: Observable<RegistrarPlanResponse>;

  async onSubmit() {
    const formVal = this.crearPlanForm.value;
    const descripcion = formVal.descripcion;
    const fecha = formVal.fecha;
    const vendedores = formVal.vendedores;
    if (
      !descripcion ||
      !fecha ||
      !(vendedores && vendedores?.length > 0) ||
      !this.crearPlanForm.valid
    ) {
      return;
    }
    const vendedoresToSend = this.vendedoresDto.filter((vendedor) =>
      vendedores.includes(vendedor.id)
    );
    this.crearPlan({
      fecha,
      descripcion,
      vendedores: vendedoresToSend,
    });
  }

  cancelar() {
    this.router.navigate(['/plan']);
  }

  crearPlan(params: RegistrarPlanProps) {
    console.log('creando plan', params);
    this.registroResponse = this.planService.registrarPlan(params);
    this.registroResponse.subscribe(async (result) => {
      console.log('vendedor creado:', result);
      this.router.navigate(['/ventas']);
    });
  }
}
