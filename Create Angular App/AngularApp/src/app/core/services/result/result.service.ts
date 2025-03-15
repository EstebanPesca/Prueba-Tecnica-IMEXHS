import { Injectable, Signal, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ResultService {

  constructor() { }

  // Instancia que almacena los resultados
  private results = signal<{ timestamp: string; points: number; area: number }[]>([]);

  /**
   * Funcion enfocada en almacenas los calculos realziados
   * @param points 
   * @param area 
   */
  public saveResult(points: number, area: number) {
    // Se crea un nuevo resultado con fecha actual, puntos ingresados y el area calculada
    const newResult = {
      timestamp: new Date().toLocaleString(),
      points,
      area
    };
    // Se actualiza el array de calculos almacenados
    this.results.update((prev) => [...prev, newResult]);
  }

  /**
   * Se solicita la informacion guardada de los calculos
   * @returns 
   */
  getResults(): Signal<{ timestamp: string; points: number; area: number }[]> {
    return this.results;
  }
}
