import { Component } from '@angular/core';

@Component({
  selector: 'app-templates',
  imports: [],
  template: `
    <input type="text" (keyup.enter)="updateField($event)" />
    @if (a > b) {
      {{a}} is greater than {{b}}
    } @else if (b > a) {
      {{a}} is less than {{b}}
    } @else {
      {{a}} is equal to {{b}}
    }
  `,
  styleUrl: './templates.component.scss'
})
export class TemplatesComponent {
  a = 1;
  b = 2;
  updateField(event: Event): void {
    console.log('The user pressed enter in the text field.');
  }
}
