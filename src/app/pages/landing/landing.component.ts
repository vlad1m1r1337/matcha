import { Component, OnInit } from '@angular/core';
import {concatMap, delay, mergeMap, of} from 'rxjs';
import { ProductService } from '../../services/product.service';

@Component({
  selector: 'app-landing',
  imports: [],
  providers: [ProductService],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.scss'
})
export class LandingComponent implements OnInit {
  constructor(private productService: ProductService) {}

  ngOnInit() {
    // this.loadProductsWithMergeMap();
    // Или можешь раскомментировать, чтобы попробовать concatMap:
    this.loadProductsWithConcatMap();
  }

  loadProductsWithMergeMap() {
    of(1, 2, 3).pipe(
      mergeMap(id => this.productService.getProductById(id).pipe(delay(1000)))
    ).subscribe(product => {
      console.log('Продукт (mergeMap):', product);
    });
  }

  loadProductsWithConcatMap() {
    of(1, 2, 3).pipe(
      concatMap(id => this.productService.getProductById(id).pipe(delay(1000)))
    ).subscribe(product => {
      console.log('Продукт (concatMap):', product);
    });
  }
}
