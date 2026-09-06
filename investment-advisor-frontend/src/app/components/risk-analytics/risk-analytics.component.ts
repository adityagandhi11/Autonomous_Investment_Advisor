import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

interface RiskMetrics {
  volatility_pct?: number;
  sharpe_ratio?: number;
  sortino_ratio?: number;
  maximum_drawdown_pct?: number;
  var_95_pct?: number;
  var_99_pct?: number;
  beta?: number;
  alpha?: number;
}

interface PortfolioRiskData {
  portfolio_summary: any;
  risk_assessment: any;
  stress_test: any;
}

@Component({
  selector: 'app-risk-analytics',
  templateUrl: './risk-analytics.component.html',
  styleUrls: ['./risk-analytics.component.css']
})
export class RiskAnalyticsComponent implements OnInit {
  selectedTickerForAnalysis = 'NIFTYBEES.NS';
  portfolioForAnalysis: { [key: string]: number } = {
    'NIFTYBEES.NS': 25000,
    'GOLDBEES.NS': 15000,
    'HDFCBANK.NS': 10000
  };

  assetRiskMetrics: RiskMetrics | null = null;
  portfolioRiskData: PortfolioRiskData | null = null;
  loadingAssetAnalysis = false;
  loadingPortfolioAnalysis = false;
  errorMessage = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Optional: Load default analysis on init
  }

  analyzeAssetRisk(): void {
    if (!this.selectedTickerForAnalysis.trim()) {
      this.errorMessage = 'Please enter a ticker symbol';
      return;
    }

    this.loadingAssetAnalysis = true;
    this.errorMessage = '';

    this.apiService.getAssetRiskMetrics(this.selectedTickerForAnalysis).subscribe(
      (data) => {
        this.assetRiskMetrics = data;
        this.loadingAssetAnalysis = false;
      },
      (error) => {
        this.errorMessage = `Error analyzing ${this.selectedTickerForAnalysis}: ${error.message}`;
        this.loadingAssetAnalysis = false;
      }
    );
  }

  analyzePortfolioRisk(): void {
    if (Object.keys(this.portfolioForAnalysis).length === 0) {
      this.errorMessage = 'Please add at least one asset to the portfolio';
      return;
    }

    this.loadingPortfolioAnalysis = true;
    this.errorMessage = '';

    this.apiService.getPortfolioRiskAnalytics(this.portfolioForAnalysis).subscribe(
      (data) => {
        this.portfolioRiskData = data;
        this.loadingPortfolioAnalysis = false;
      },
      (error) => {
        this.errorMessage = `Error analyzing portfolio: ${error.message}`;
        this.loadingPortfolioAnalysis = false;
      }
    );
  }

  addAssetToPortfolio(): void {
    const ticker = prompt('Enter ticker symbol (e.g., RELIANCE.NS):');
    const amount = prompt('Enter investment amount (₹):');

    if (ticker && amount) {
      this.portfolioForAnalysis[ticker.toUpperCase()] = parseFloat(amount);
    }
  }

  removeAssetFromPortfolio(ticker: string): void {
    delete this.portfolioForAnalysis[ticker];
  }

  getPortfolioAssets(): Array<{ ticker: string; amount: number }> {
    return Object.entries(this.portfolioForAnalysis).map(([ticker, amount]) => ({
      ticker,
      amount
    }));
  }

  getRiskLevel(volatility?: number): string {
    if (!volatility) return 'Unknown';
    if (volatility < 10) return 'Low';
    if (volatility < 20) return 'Moderate';
    if (volatility < 30) return 'High';
    return 'Very High';
  }

  getSharpeInterpretation(sharpe?: number): string {
    if (sharpe === undefined) return '';
    if (sharpe > 1) return 'Excellent';
    if (sharpe > 0.5) return 'Good';
    if (sharpe > 0) return 'Acceptable';
    return 'Poor';
  }

  getDrawdownInterpretation(drawdown?: number): string {
    if (!drawdown) return '';
    return `Lost up to ${Math.abs(drawdown).toFixed(1)}% from peak`;
  }
}
