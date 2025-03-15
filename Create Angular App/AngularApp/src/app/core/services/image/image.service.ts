import { Injectable, signal, Signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  constructor() { }

  // Semaneja el estado de la imagen
  private imageSrc = signal<string | null>(null);

  // Guardamos la imagen
  public setImage(src: string) {
    this.imageSrc.set(src);
  }

  // Retornamos la imagen a otros componentes
  public getImage(): Signal<string | null> {
    return this.imageSrc;
  }

}
