import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface InvestmentRequest {
  user_goal: string;
  investment_amount: number;
  duration_years: number;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly apiUrl = environment.apiUrl.replace(/\/$/, '');

  constructor(private http: HttpClient) {}

  getData(endpoint: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/${endpoint.replace(/^\//, '')}`);
  }

  postData(endpoint: string, data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/${endpoint.replace(/^\//, '')}`, data);
  }

  analyzeInvestment(request: InvestmentRequest): Observable<any> {
    return this.postData('invest', request);
  }

  // ============ Market Data APIs ============
  
  getRealtimePrice(ticker: string): Observable<any> {
    return this.getData(`market/price/${ticker}`);
  }

  getMarketData(ticker: string, period: string = '1mo'): Observable<any> {
    return this.getData(`market/data/${ticker}?period=${period}`);
  }

  getMultipleMarketData(tickers: string[], period: string = '1mo'): Observable<any> {
    return this.postData('market/data-multiple', { tickers, period });
  }

  getCacheStats(): Observable<any> {
    return this.getData('market/cache-stats');
  }

  clearCache(): Observable<any> {
    return this.postData('market/cache-clear', {});
  }

  // ============ Risk Analytics APIs ============

  getAssetRiskMetrics(ticker: string, period: string = '3mo'): Observable<any> {
    return this.getData(`analytics/asset-risk/${ticker}?period=${period}`);
  }

  getPortfolioRiskAnalytics(portfolio: { [key: string]: number }): Observable<any> {
    return this.postData('analytics/portfolio-risk', portfolio);
  }

  calculateSharpeRatio(returns: number[]): Observable<any> {
    return this.postData('analytics/sharpe-ratio', { returns });
  }

  calculateVolatility(returns: number[]): Observable<any> {
    return this.postData('analytics/volatility', { returns });
  }

  getCorrelationMatrix(tickers: string[], period: string = '1mo'): Observable<any> {
    return this.postData('analytics/correlation-matrix', { tickers, period });
  }

  runStressTest(portfolio: { [key: string]: number }, scenario: string = 'market_down_10'): Observable<any> {
    return this.postData('analytics/stress-test', { portfolio, scenario });
  }

  calculateMaximumDrawdown(priceHistory: number[]): Observable<any> {
    return this.postData('analytics/maximum-drawdown', { price_history: priceHistory });
  }

  calculateValueAtRisk(returns: number[], confidenceLevel: number = 0.95): Observable<any> {
    return this.postData('analytics/value-at-risk', { returns, confidence_level: confidenceLevel });
  }

  getPortfolioMetrics(portfolio: { [key: string]: number }): Observable<any> {
    return this.postData('analytics/portfolio-metrics', portfolio);
  }

  // Additional methods for PUT, DELETE, etc. can be added here
}