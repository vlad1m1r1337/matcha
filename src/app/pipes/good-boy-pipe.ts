import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'goodBoy' })
export class GoodBoyPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return value;  // если пустая строка, возвращаем её
    return value
      .concat(' - Красавчик !')
  }
}
