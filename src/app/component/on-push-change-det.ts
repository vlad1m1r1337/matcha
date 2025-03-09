import { Component, Input, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-onpush-cd',
  template: `
    <div>
      <h2>OnPush Change Detection</h2>
      <p>Счётчик: {{ counter.value }}</p>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OnPushCdComponent {
  @Input() counter: { value: number } = { value: 0 };

}
