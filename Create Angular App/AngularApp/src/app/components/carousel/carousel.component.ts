import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-carousel',
  standalone:true,
  imports: [CommonModule],
  templateUrl: './carousel.component.html',
  styleUrl: './carousel.component.css'
})
export class CarouselComponent {

  // Paso a paso que se mostrara en el carousel
  public steps = [
    {
      title: 'Step 1: Upload a image',
      description: 'Select a binary image.',
      image: 'step1.png'
    },
    {
      title: 'Step 2: Generate Random Points',
      description: 'Select the number of points in the slider.',
      image: 'step2.png'
    },
    {
      title: 'Step 2: Generate Random Points',
      description: 'Press the buttom "Generate Points".',
      image: 'step3.png'
    },
    {
      title: 'Step 4: Contar los Puntos en la Mancha',
      description: 'Press the buttom "Calculate Area".',
      image: 'step4.png'
    },
    {
      title: 'Step 5(Optional): See historial',
      description: 'View your latest calculations.',
      image: 'step5.png'
    }
  ]

}
