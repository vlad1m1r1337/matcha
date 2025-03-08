import { Component } from '@angular/core';
import {CommonModule} from '@angular/common';
import {GoodBoyPipe} from '../../pipes/good-boy-pipe';

@Component({
  selector: 'app-pipe',
  imports: [CommonModule, GoodBoyPipe],
  template: `
    <p>{{ 'Hello World' | lowercase }}</p>
    <p>{{ 'Hello World' | uppercase }}</p>
    <p>{{ 'Vova' | goodBoy }}</p>
    <p>{{ 1234567890 | number }}</p>
    <div *ngIf="isVisible">Привет, Angular!</div>
    <button (click)="isVisible = !isVisible">Показать/скрыть</button>
    <li *ngFor="let item of items">{{ item }}</li>
    <p [ngStyle]="{ 'background-color': color }">RED</p>
  `,
  styleUrl: './pipe.component.scss'
})
export class PipeComponent {
  isVisible = true;
  items= ['a', 'b', 'c'];
  color = 'red';
}
