import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { UploadComponent } from './components/upload/upload.component';
import { PointGeneratorComponent } from './components/point-generator/point-generator.component';
import { AreaCalculatorComponent } from './components/area-calculator/area-calculator.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, UploadComponent, PointGeneratorComponent, AreaCalculatorComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'AngularApp';
}
