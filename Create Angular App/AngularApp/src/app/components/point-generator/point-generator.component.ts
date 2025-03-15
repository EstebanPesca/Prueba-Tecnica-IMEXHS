import { Component, inject, Signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// Materials
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';

// Services
import { PointService } from '../../core/services/point/point.service';
import { ImageService } from '../../core/services/image/image.service';

@Component({
  selector: 'app-point-generator',
  imports: [
    CommonModule, 
    MatSliderModule, 
    MatButtonModule,
    FormsModule,
  ],
  templateUrl: './point-generator.component.html',
  styleUrl: './point-generator.component.css'
})
export class PointGeneratorComponent {

  // Instanciamos los servicios
  public _pointService = inject(PointService);
  public _imageService = inject(ImageService);

  // Se obtiene la cantidad de puntos que se mostraran en la imagen
  public points: Signal<{ x: number; y: number }[]> = this._pointService.getPoints();
  // Contador de puntos
  public pointCount = 100;

  /**
   * Funcion enfocada en actualizar los puntos mediantes el slider
   * @param event 
   */
  public updatePointCount(event: any) {
    // Instanciamos el input del slider
    const target = event.target as HTMLInputElement | null;
    // Validamos que exista el input
    if (target) {
      // Encapsulamos el value
      const newValue = target.valueAsNumber;
      // Reasignamos el numero de puntos
      this.pointCount = isNaN(newValue) ? 100 : newValue;
    }
  }

  /**
   * Funcion enfocada en generar de forma random los puntos
   */
  public generatePoints() {
    // Instanciamos la imagen
    const img = new Image();
    // Se asigna ubicacion de la imagen
    img.src = this._imageService.getImage()() || '';
    // Se muestra en pantala la imagen
    img.onload = () => {
      // Llamamos al servicio para generar los puntos
      this._pointService.generatePoints(this.pointCount, img.width, img.height);
    };
  }

}
