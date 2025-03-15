import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PointGeneratorComponent } from './point-generator.component';

describe('PointGeneratorComponent', () => {
  let component: PointGeneratorComponent;
  let fixture: ComponentFixture<PointGeneratorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PointGeneratorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PointGeneratorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
