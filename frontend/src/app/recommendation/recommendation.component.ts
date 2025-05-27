import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-recommendation',
  templateUrl: './recommendation.component.html'
})
export class RecommendationComponent {
  user = {
    price: 10000000,
    area: '',
    propertyType: 'Villa',
    inventoryType: 'Ready to Move',
    bhk: 2,
    furnishing: 'Fully Furnished',
    reraApproved: true,
    possession: 'Ready to Move',
    facing: 'North'
  };

  recommendations: any[] = [];

  constructor(private http: HttpClient) {}

  getRecommendations() {
    this.http.post<any[]>('http://localhost:5000/recommend', this.user)
      .subscribe(data => this.recommendations = data);
  }
}
