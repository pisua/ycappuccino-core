import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['../assets/styles/main.scss'],
  encapsulation : ViewEncapsulation.None
})
export class AppComponent {
  title = 'angular-tutorial';
}
