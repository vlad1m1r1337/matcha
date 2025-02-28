import { Routes } from '@angular/router';
import { LandingComponent } from './pages/landing/landing.component';
import { LoginComponent } from './pages/login/login.component';
import {RegisterComponent} from './pages/register/register.component';
import {NotFoundComponent} from './pages/not-found/not-found.component';

export const routes: Routes = [
  { path: '', component: LandingComponent, runGuardsAndResolvers: 'always' }, // Главная страница
  { path: 'login', component: LoginComponent, runGuardsAndResolvers: 'always' }, // Страница входа
  { path: 'registr', component: RegisterComponent, runGuardsAndResolvers: 'always' }, // Страница входа
  { path: '**', component: NotFoundComponent, runGuardsAndResolvers: 'always' } // Перенаправление на главную для неизвестных маршрутов
];
