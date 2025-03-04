import { Injectable } from '@angular/core';
import { of } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ProductService {
  getProductById(id: number) {
    return of({ id, name: `Товар ${id}`, price: id * 10 });
  }
}
