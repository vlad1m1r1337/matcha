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
  `,
  styleUrl: './pipe.component.scss'
})
export class PipeComponent {

}
