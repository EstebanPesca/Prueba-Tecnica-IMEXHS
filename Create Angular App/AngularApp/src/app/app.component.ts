import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

// Components
import { UploadComponent } from './components/upload/upload.component';
import { PointGeneratorComponent } from './components/point-generator/point-generator.component';
import { AreaCalculatorComponent } from './components/area-calculator/area-calculator.component';
import { ResultsTableComponent } from './components/results-table/results-table.component';

// Materiasl
import { MatTabsModule } from '@angular/material/tabs';
import { CarouselComponent } from './components/carousel/carousel.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,
    UploadComponent,
    PointGeneratorComponent,
    AreaCalculatorComponent,
    ResultsTableComponent,
    MatTabsModule,
    CarouselComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'AngularApp';
}
