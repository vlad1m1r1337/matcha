import { Routes } from '@angular/router';
import { LandingComponent } from './pages/landing/landing.component';
import { LoginComponent } from './pages/login/login.component';
import {PipeComponent} from './pages/pipe/pipe.component';
import {NotFoundComponent} from './pages/not-found/not-found.component';
import {TemplatesComponent} from './pages/templates/templates.component';
import {BindingComponent} from './pages/binding/binding.component';
import {ChangeDetectionComponent} from './pages/change-detection/change-detection.component';

export const routes: Routes = [
  { path: '', component: LandingComponent, runGuardsAndResolvers: 'always' },
  { path: 'pipe', component: PipeComponent, runGuardsAndResolvers: 'always' },
  { path: 'change_det', component: ChangeDetectionComponent, runGuardsAndResolvers: 'always' },
  { path: 'templates', component: TemplatesComponent, runGuardsAndResolvers: 'always' },
  { path: 'binding', component: BindingComponent, runGuardsAndResolvers: 'always' },
  { path: 'login', component: LoginComponent, runGuardsAndResolvers: 'always' },
  { path: 'registr', loadChildren: () => import('./pages/registr/registr.module').then(m => m.RegisterModule), runGuardsAndResolvers: 'always' },
  { path: '**', component: NotFoundComponent, runGuardsAndResolvers: 'always' } // Перенаправление на главную для неизвестных маршрутов
];
