import {ChangeDetectionStrategy, Component} from '@angular/core';
import {DefaultCdComponent} from '../../component/def-change-det';
import {OnPushCdComponent} from '../../component/on-push-change-det';

@Component({
  selector: 'app-change-detection',
  imports: [DefaultCdComponent, OnPushCdComponent],
  template: `
    <h1>Change Detection Example</h1>
    <button (click)="increment()">Увеличить счётчик</button>

    <app-default-cd (counterChange)="receiveMessage($event)" [counter]="counter"></app-default-cd>
    <app-onpush-cd [counter]="counter"></app-onpush-cd>
  `,
  styleUrl: './change-detection.component.scss'
})
export class ChangeDetectionComponent {
  counter = { value: 0 };
  message = { value: 0 };
  increment() {
    this.counter.value++;
  }

  receiveMessage(event: { value: number }) {
    this.message = event;
  }

  ngDoCheck() {
    console.log(this.counter);
  }
}
