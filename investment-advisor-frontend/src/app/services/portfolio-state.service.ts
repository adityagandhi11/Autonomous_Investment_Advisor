import { Injectable } from '@angular/core';

export interface PortfolioDashboardState {
  data: any;

  investmentGoal: string;
  investmentAmount: number;
  durationYears: number;

  conversationId: string | null;

  chatMessages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;

  guestMessageCount: number;
}

@Injectable({
  providedIn: 'root'
})
export class PortfolioStateService {

  private readonly STORAGE_KEY =
    'investment_advisor_dashboard_state';

  constructor() {}

  saveState(state: PortfolioDashboardState): void {
    try {
      sessionStorage.setItem(
        this.STORAGE_KEY,
        JSON.stringify(state)
      );
    } catch (error) {
      console.error(
        'Unable to save dashboard state:',
        error
      );
    }
  }

  getState(): PortfolioDashboardState | null {
    try {
      const savedState =
        sessionStorage.getItem(this.STORAGE_KEY);

      if (!savedState) {
        return null;
      }

      return JSON.parse(savedState);
    } catch (error) {
      console.error(
        'Unable to restore dashboard state:',
        error
      );

      return null;
    }
  }

  hasState(): boolean {
    return sessionStorage.getItem(this.STORAGE_KEY) !== null;
  }

  clearState(): void {
    sessionStorage.removeItem(this.STORAGE_KEY);
  }
}