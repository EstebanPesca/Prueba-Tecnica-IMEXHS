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

  private imageService = inject(ImageService);

  constructor(
    private _imageService: ImageService
  ){}
  
  imageSrc: Signal<string | null> = this.imageService.getImage();

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this._imageService.setImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  }

}
