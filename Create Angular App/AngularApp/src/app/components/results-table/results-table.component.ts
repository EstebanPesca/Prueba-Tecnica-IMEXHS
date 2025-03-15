import { CommonModule } from '@angular/common';
import { Component, inject, Signal, signal } from '@angular/core';

// Materials
import { MatTableModule } from '@angular/material/table';

// Services
import { ResultService } from '../../core/services/result/result.service'

@Component({
  selector: 'app-results-table',
  imports: [CommonModule, MatTableModule],
  templateUrl: './results-table.component.html',
  styleUrl: './results-table.component.css'
})
export class ResultsTableComponent {

  // Se instancia servicios
  private _resultsService = inject(ResultService);

  // Solicitamos los resultados obtenidos por el calculo de los puntos por mancha
  public results: Signal<{ timestamp: string; points: number; area: number }[]> = this._resultsService.getResults();

  // Nombre de las columnas
  public displayedColumns: string[] = ['timestamp', 'points', 'area'];

}
