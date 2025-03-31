import { Component } from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import { NavbarComponent } from "../navbar/navbar.component";
import { LOCALE_ID, Inject, ɵsetLocaleId } from '@angular/core';
import {MatMenuModule} from '@angular/material/menu';

@Component({
  selector: 'app-header',
  imports: [MatToolbarModule, MatButtonModule, MatIconModule, NavbarComponent, MatMenuModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

  selectedLocale: string
  availableLocales: string[] = ["es", "en-US"]

  constructor(
    @Inject(LOCALE_ID) public locale: string
  ) { 
    this.selectedLocale = locale
  }

  setLocale(localeId: string){
    ɵsetLocaleId(localeId)
  }
}
