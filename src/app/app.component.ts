import { Component } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import { AuthService } from './service';
import {RouterOutlet} from '@angular/router'; // Add this line

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ReactiveFormsModule, RouterOutlet],  // Добавляем ReactiveFormsModule
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  loginForm: FormGroup;
  message = '';

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.loginForm = this.fb.group({
      name: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const name = this.loginForm.value.name;
      this.authService.login(name).subscribe({
        next: (response) => {
          this.message = response.message;
        },
        error: (err) => {
          this.message = err.error.message || 'Ошибка входа';
        }
      });
    }
  }
}
