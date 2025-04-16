import { Component } from '@angular/core';
import * as versionJson from '../../../public/version.json'

@Component({
  selector: 'app-footer',
  imports: [],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent {
  versionJson = versionJson
}
