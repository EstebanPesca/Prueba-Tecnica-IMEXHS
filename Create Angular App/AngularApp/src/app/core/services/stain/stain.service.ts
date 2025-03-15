import { Injectable, signal, Signal } from '@angular/core';
import { PointService } from '../point/point.service';
import { ImageService } from '../image/image.service';

@Injectable({
  providedIn: 'root'
})
export class StainService {

  // Se almacena el estimado de puntos en la mancha
  private estimatedArea = signal<number | null>(null);

  constructor(
    private _pointService: PointService, 
    private _imageService: ImageService
  ) {}

  /**
   * 
   * @returns 
   */
  public calculateStainArea() {
    // Se crea una instancia de la imagen que se subio
    const imageSrc = this._imageService.getImage()();
    // Se valida que exista una imagen
    if (!imageSrc) return;

    // Se crea nueva instancia de imagen
    const img = new Image();
    // Se le asigna a la imagen la ubicacion de la imagen subida por el usuario
    img.src = imageSrc;
    img.onload = () => {
      // Se crea un canvas para realizar el calculo
      const canvas = document.createElement('canvas');
      // Se asigna anchor y altura al canvas
      canvas.width = img.width;
      canvas.height = img.height;
      // Se le define referencia de dimensiones
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      // Se solicitar replicar la imagen en el canvas
      ctx.drawImage(img, 0, 0, img.width, img.height);
      const imageData = ctx.getImageData(0, 0, img.width, img.height).data;

      // Se instancia el array de los puntos generados aleatoriamente
      const points = this._pointService.getPoints()();
      let ni = 0;

      // Se recorre el array de puntos
      for (const point of points) {
        const index = (point.y * img.width + point.x) * 4;
        const red = imageData[index];
        const green = imageData[index + 1];
        const blue = imageData[index + 2];

        // Si el píxel es blanco (R=255, G=255, B=255), el punto está dentro de la mancha
        if (red === 255 && green === 255 && blue === 255) {
          ni++;
        }
      }

      // Realizamos el calculo del area total de la imagen
      const totalArea = img.width * img.height;
      // Realizamos el calculo de la mancha
      const estimatedArea = totalArea * (ni / points.length);
      // Almacenamos el valor obtenido
      this.estimatedArea.set(estimatedArea);
    };
  }

  public getEstimatedArea(): Signal<number | null> {
    return this.estimatedArea;
  }
}
