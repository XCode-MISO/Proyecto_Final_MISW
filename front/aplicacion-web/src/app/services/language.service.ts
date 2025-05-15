import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LanguageService {
  private currentLang = new BehaviorSubject<string>('es');
  currentLang$ = this.currentLang.asObservable();

  constructor(private translate: TranslateService) {
    const savedLang = localStorage.getItem('selectedLanguage') || 'es';
    this.setLanguage(savedLang);
  }

  setLanguage(lang: string): void {
  
    localStorage.setItem('selectedLanguage', lang);
    this.translate.use(lang);
    this.currentLang.next(lang);
  }

  getCurrentLanguage(): string {
    return this.currentLang.value;
  }

  getAvailableLanguages(): { code: string, name: string }[] {
    return [
      { code: 'es', name: 'Español' },
      { code: 'en-US', name: 'English' }
    ];
  }
}