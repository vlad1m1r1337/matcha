import {Component, EventEmitter, Input, Output} from '@angular/core';

@Component({
  selector: 'app-default-cd',
  template: `
    <div>
      <h2>Default Change Detection</h2>
      <p>Счётчик: {{ counter.value }}</p>
    </div>
  `,
})
export class DefaultCdComponent {
  @Input() counter: { value: number } = { value: 0 };
  @Output() counterChange = new EventEmitter<{ value: number }>();
}
