import { Injectable, Signal, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PointService {

  constructor() { }

  // Array de duplas con posicion de cada punto
  private points = signal<{x: number, y: number}[]>([]);

  /**
   * Se crean puntos aleatorios
   * @param n cantidad de n veces por el que crearan los puntos
   * @param width 
   * @param height 
   */
  public generatePoints(n:number, width: number, height: number){
    // Se crea un array con los puntos donde se pondran los puntos
    const newPoints = Array.from({ length: n }, () => ({
      x: Math.floor(Math.random() * width),
      y: Math.floor(Math.random() * height)
    }));
    // Se almacena el array de puntos
    this.points.set(newPoints);
  }

  /**
   * Se retorna los points
   * @returns 
   */
  public getPoints(): Signal<{ x: number; y: number }[]> {
    return this.points;
  }

}
