import { Component } from '@angular/core';
import {LoginHeaderComponent} from '../../component/login.header';
import {LoginMainComponent} from '../../component/login.main';

@Component({
  selector: 'app-login',
  imports: [LoginHeaderComponent, LoginMainComponent],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {

}
