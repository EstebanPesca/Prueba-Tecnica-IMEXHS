import { Component, inject, Signal } from '@angular/core';
import { CommonModule } from '@angular/common';

// Materials
import { MatButtonModule } from '@angular/material/button';

// Servicies
import { StainService } from '../../core/services/stain/stain.service';
import { ImageService } from '../../core/services/image/image.service';

@Component({
  selector: 'app-area-calculator',
  standalone:true,
  imports: [CommonModule, MatButtonModule],
  templateUrl: './area-calculator.component.html',
  styleUrl: './area-calculator.component.css'
})
export class AreaCalculatorComponent {

  // Se instancian los servicios 
  private _stainService = inject(StainService);
  public _imageService = inject(ImageService);

  // Se obtiene el calculo estimado de la cantidad de puntos en la mancha
  public estimatedArea: Signal<number | null> = this._stainService.getEstimatedArea();

  /**
   * Se solicita el calculo de la cantidad de puntos en la mancha
   */
  public calculateArea() {
    this._stainService.calculateStainArea();
  }

}
