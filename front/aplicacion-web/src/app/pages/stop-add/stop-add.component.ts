import {ChangeDetectionStrategy, Component, signal} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { Cliente } from '../routes/routes.component';

@Component({
  selector: 'app-stop-add',
  imports: [MatFormFieldModule, MatInputModule, MatSelectModule, MatButtonModule, MatDatepickerModule],
  templateUrl: './stop-add.component.html',
  styleUrl: './stop-add.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StopAddComponent {

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

  protected readonly value = signal('');
  protected onInput(event: Event) {
    this.value.set((event.target as HTMLInputElement).value);
  }
}
