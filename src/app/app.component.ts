import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from './service';
import {RouterLink, RouterOutlet} from '@angular/router';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators'; // Add RxJS operators

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
    </router-outlet>
  `,
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'lalalend'
}
