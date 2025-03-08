import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import {RouterLink, RouterOutlet} from '@angular/router';
import {LoggerService} from './service';



@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ReactiveFormsModule, RouterOutlet, RouterLink],
  template: `
    <router-outlet>
      <a [routerLink]="['/']">Главная</a>
      <a [routerLink]="['/login']">Логин</a>
      <a [routerLink]="['/registr']">Регистрация</a>
      <a [routerLink]="['/pipe']">Pipe</a>
      <a [routerLink]="['/templates']">Templates</a>
    </router-outlet>
  `,
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor(private logger: LoggerService) {
    this.logger.log('Компонент инициализирован!');
  }
}
