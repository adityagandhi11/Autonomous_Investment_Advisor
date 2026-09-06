import { Component, OnInit } from '@angular/core';
import { ApiService, InvestmentRequest } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  data: any;
  investmentGoal = 'I want to invest for long-term wealth creation';
  investmentAmount = 50000;
  durationYears = 5;
  isLoading = false;
  errorMessage = '';
  submitted = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.data = undefined;
    this.submitted = false;
    this.errorMessage = '';
  }

  analyzePortfolio(): void {
    if (!this.investmentGoal.trim() || this.investmentAmount < 1000 || this.durationYears < 1) {
      this.errorMessage = 'Enter a goal, an amount of at least ₹1,000, and a valid horizon.';
      return;
    }

    const request: InvestmentRequest = {
      user_goal: this.investmentGoal.trim(),
      investment_amount: Number(this.investmentAmount),
      duration_years: Number(this.durationYears)
    };

    this.isLoading = true;
    this.submitted = true;
    this.errorMessage = '';
    this.apiService.analyzeInvestment(request).subscribe(response => {
      this.data = response;
      this.isLoading = false;
    }, error => {
      this.isLoading = false;
      this.errorMessage = error.error && error.error.detail
        ? error.error.detail
        : 'Unable to complete the analysis. Check that FastAPI is running on port 8000.';
    });
  }

  allocationEntries(): Array<{ name: string; amount: number }> {
    if (!this.data || !this.data.portfolio) {
      return [];
    }
    return Object.keys(this.data.portfolio).map(name => ({
      name,
      amount: Number(this.data.portfolio[name])
    }));
  }

  allocationTotal(): number {
    return this.allocationEntries().reduce((total, item) => total + item.amount, 0);
  }

  allocationPercent(amount: number): number {
    const total = this.allocationTotal();
    return total ? (amount / total) * 100 : 0;
  }

  getRecommendations(): any[] {
    if (!this.data || !this.data.recommendations) {
      return [];
    }
    return this.data.recommendations;
  }

  exportResults(): void {
    if (!this.data) {
      return;
    }
    const blob = new Blob([JSON.stringify(this.data, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'investment-analysis.json';
    link.click();
    window.URL.revokeObjectURL(url);
  }
}