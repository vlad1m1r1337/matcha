import { Component } from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-binding',
  imports: [CommonModule, FormsModule],
  templateUrl: './binding.component.html',
  styleUrl: './binding.component.scss'
})
export class BindingComponent {
  title = 'Binding';
  body = 'This is the body content';
  message = 'Initial message';
  experiments = [
    { id: 1, name: 'Experiment 1' },
    { id: 2, name: 'Experiment 2' },
    { id: 3, name: 'Experiment 3' }
  ];

  updateMessage(newMessage: string): void {
    this.message = newMessage;
  }

  hero = false;
  heroes = ['Vova', 'Vlad', 'Viktor'];
  toeChoice = 'Eenie';
}
