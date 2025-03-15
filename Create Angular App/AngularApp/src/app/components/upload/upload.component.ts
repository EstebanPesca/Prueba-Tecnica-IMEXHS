import { CommonModule } from '@angular/common';
import { Component, Signal, inject } from '@angular/core';

// Materials
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';

// Services
import { ImageService } from '../../core/services/image/image.service';

@Component({
  selector: 'app-upload',
  standalone:true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,    
  ],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.css'
})
export class UploadComponent {

  // instanciamos el servicio
  private _imageService = inject(ImageService);
  
  // Se almacena la imagen para mostrarla posteriormente
  public imageSrc: Signal<string | null> = this._imageService.getImage();

  onFileSelected(event: Event) {
    // Cupturamos la imagen seleccionada por el usuario
    const file = (event.target as HTMLInputElement).files?.[0];
    // Validamos que contenga informacion
    if (file) {
      // Instancimos un lector de archivos
      const reader = new FileReader();
      // Guardamos la imagen
      reader.onload = () => {
        this._imageService.setImage(reader.result as string);
      };
      // Guardamos la imagen de forma local
      reader.readAsDataURL(file);
    }
  }

}
