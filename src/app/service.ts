import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root', // Глобальный провайдер
})
export class LoggerService {
  log(message: string) {
    console.log(`[Logger]: ${message}`);
  }
}
