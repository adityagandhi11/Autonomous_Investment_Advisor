import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import {
  ApiService,
  InvestmentRequest
} from '../../services/api.service';

import { AuthService } from '../../services/auth.service';
import { User } from '../../models/auth';

import { PortfolioStateService } from '../../services/portfolio-state.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  data: any;

  investmentGoal =
    'I want to invest for long-term wealth creation';

  investmentAmount = 50000;

  durationYears = 5;

  isLoading = false;
  isChatLoading = false;

  errorMessage = '';

  submitted = false;

  currentUser: User | null = null;
  isAuthenticated = false;

  conversationId: string | null = null;

  chatMessage = '';

  chatMessages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }> = [];

  guestMessageCount = 0;

  showAuthModal = false;

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private portfolioStateService: PortfolioStateService,
    private router: Router
  ) {}

  ngOnInit(): void {

    this.loadAuthenticationState();

    /*
     * First try to restore the previous dashboard state.
     *
     * This is important when the user:
     *
     * Dashboard
     *    -> Login / Signup
     *    -> Dashboard
     *
     * Without this restoration the portfolio would disappear
     * because DashboardComponent gets recreated.
     */
    const restored = this.restoreDashboardState();

    if (!restored) {
      this.fetchData();
    }
  }

  get hasAnalysis(): boolean {
    return !!this.data;
  }

  loadAuthenticationState(): void {

    this.isAuthenticated =
      this.authService.isAuthenticated();

    this.currentUser =
      this.authService.getUser();
  }

  /**
   * Restore portfolio/dashboard state from sessionStorage.
   */
  restoreDashboardState(): boolean {

    const savedState =
      this.portfolioStateService.getState();

    if (!savedState) {
      return false;
    }

    console.log(
      'Restoring previous investment dashboard state.'
    );

    this.data = savedState.data;

    this.investmentGoal =
      savedState.investmentGoal;

    this.investmentAmount =
      savedState.investmentAmount;

    this.durationYears =
      savedState.durationYears;

    this.conversationId =
      savedState.conversationId;

    this.chatMessages =
      savedState.chatMessages || [];

    this.guestMessageCount =
      savedState.guestMessageCount || 0;

    /*
     * If data exists, the portfolio analysis has already
     * been completed.
     */
    this.submitted = !!this.data;

    this.errorMessage = '';

    this.isLoading = false;

    this.isChatLoading = false;

    return true;
  }

  /**
   * Save the current dashboard state.
   */
  saveDashboardState(): void {
    const state = {
      data: this.data,
      investmentGoal: this.investmentGoal,
      investmentAmount: Number(this.investmentAmount),
      durationYears: Number(this.durationYears),
      conversationId: this.conversationId,
      chatMessages: this.chatMessages,
      guestMessageCount: this.guestMessageCount
    };

    console.log('SAVING DASHBOARD STATE:', state);

    try {
      sessionStorage.setItem(
        'investment_advisor_dashboard_state',
        JSON.stringify(state)
      );

      console.log(
        'SESSION STORAGE:',
        sessionStorage.getItem(
          'investment_advisor_dashboard_state'
        )
      );
    } catch (error) {
      console.error(
        'SESSION STORAGE ERROR:',
        error
      );
    }
  }
  /**
   * Clear the dashboard state.
   *
   * Used when the user explicitly logs out.
   */
  clearDashboardState(): void {

    this.portfolioStateService.clearState();

    this.data = undefined;

    this.submitted = false;

    this.chatMessages = [];

    this.chatMessage = '';

    this.conversationId = null;

    this.guestMessageCount = 0;
  }

  goToLogin(): void {

    /*
     * Save the portfolio before leaving the dashboard.
     */
    this.saveDashboardState();

    this.router.navigate(
      ['/login'],
      {
        queryParams: {
          returnUrl: '/dashboard'
        }
      }
    );
  }

  goToSignup(): void {

    /*
     * Save the portfolio before leaving the dashboard.
     */
    this.saveDashboardState();

    this.router.navigate(
      ['/signup'],
      {
        queryParams: {
          returnUrl: '/dashboard'
        }
      }
    );
  }

  logout(): void {

    this.authService.logout();

    this.isAuthenticated = false;

    this.currentUser = null;

    /*
     * Once the user explicitly logs out, remove the
     * temporary dashboard state as well.
     */
    this.clearDashboardState();

    this.showAuthModal = false;
  }

  /**
   * Reset dashboard to its initial state.
   *
   * This method intentionally does NOT clear sessionStorage
   * unless explicitly requested.
   */
  fetchData(): void {

    this.data = undefined;

    this.submitted = false;

    this.errorMessage = '';

    this.chatMessages = [];

    this.chatMessage = '';

    this.conversationId = null;

    this.isLoading = false;

    this.isChatLoading = false;

    this.guestMessageCount = 0;
  }

  analyzePortfolio(): void {

    if (
      !this.investmentGoal.trim() ||
      this.investmentAmount < 1000 ||
      this.durationYears < 1
    ) {
      this.errorMessage =
        'Enter a goal, an amount of at least ₹1,000, and a valid horizon.';

      return;
    }

    const request: InvestmentRequest = {

      user_goal:
        this.investmentGoal.trim(),

      investment_amount:
        Number(this.investmentAmount),

      duration_years:
        Number(this.durationYears)
    };

    this.isLoading = true;

    this.submitted = true;

    this.errorMessage = '';

    /*
     * A new analysis gets a fresh conversation.
     */
    this.conversationId = null;

    this.chatMessages = [];

    this.apiService
      .analyzeInvestment(request)
      .subscribe(
        response => {

          this.data = response;

          this.isLoading = false;

          /*
           * Initial assistant message.
           */
          this.chatMessages = [
            {
              role: 'assistant',

              content:
                'Your portfolio is ready. I can explain the strategy, answer questions about individual assets, or help you adjust the investment plan.'
            }
          ];

          /*
           * IMPORTANT:
           *
           * Save the generated portfolio immediately.
           *
           * If the user now goes to Login/Signup,
           * the portfolio can be restored.
           */
          this.saveDashboardState();
        },

        error => {

          this.isLoading = false;

          this.errorMessage =
            error.error &&
            error.error.detail
              ? error.error.detail
              : 'Unable to complete the analysis. Check that FastAPI is running on port 8000.';
        }
      );
  }

  // sendChatMessage(): void {

  //   const message =
  //     this.chatMessage.trim();

  //   if (
  //     !message ||
  //     this.isChatLoading
  //   ) {
  //     return;
  //   }

  //   /*
  //    * ------------------------------------------------
  //    * GUEST USER
  //    * ------------------------------------------------
  //    */

  //   if (!this.isAuthenticated) {

  //     /*
  //      * Guest gets exactly one free chat message.
  //      *
  //      * On the second attempt, show Login/Signup modal.
  //      */
  //     if (this.guestMessageCount >= 1) {

  //       /*
  //        * Save portfolio before showing auth modal.
  //        */
  //       this.saveDashboardState();

  //       this.showAuthModal = true;

  //       return;
  //     }

  //     this.addUserMessage(message);

  //     this.chatMessage = '';

  //     this.guestMessageCount++;

  //     this.addAssistantMessage(
  //       'Please log in or sign up to continue chatting with your investment advisor.'
  //     );

  //     /*
  //      * Save guest state as well.
  //      *
  //      * This means the guest's portfolio and chat
  //      * remain available after Login/Signup.
  //      */
  //     this.saveDashboardState();

  //     return;
  //   }

  //   /*
  //    * ------------------------------------------------
  //    * AUTHENTICATED USER
  //    * ------------------------------------------------
  //    */

  //   this.addUserMessage(message);

  //   this.chatMessage = '';

  //   this.isChatLoading = true;

  //   this.errorMessage = '';

  //   const request = {

  //     conversation_id:
  //       this.conversationId,

  //     message:
  //       message,

  //     investment_goal:
  //       this.investmentGoal,

  //     investment_amount:
  //       Number(this.investmentAmount),

  //     duration_years:
  //       Number(this.durationYears),

  //     risk_profile:
  //       this.data?.risk_profile || null,

  //     portfolio:
  //       this.data?.portfolio || null
  //   };

  //   this.apiService
  //     .sendChatMessage(request)
  //     .subscribe(

  //       response => {

  //         this.conversationId =
  //           response.conversation_id;

  //         this.addAssistantMessage(
  //           response.message
  //         );

  //         this.isChatLoading = false;

  //         /*
  //          * Save updated conversation state.
  //          */
  //         this.saveDashboardState();
  //       },

  //       error => {

  //         this.isChatLoading = false;

  //         this.errorMessage =
  //           error.error &&
  //           error.error.detail
  //             ? error.error.detail
  //             : 'Unable to send your message. Please try again.';

  //         this.addAssistantMessage(
  //           'I was unable to process that message. Please try again.'
  //         );

  //         /*
  //          * Preserve the chat even if the API call fails.
  //          */
  //         this.saveDashboardState();
  //       }
  //     );
  // }

  sendChatMessage(): void {
  const message = this.chatMessage.trim();

  if (!message || this.isChatLoading) {
    return;
  }

  if (!this.isAuthenticated) {
    if (this.guestMessageCount >= 1) {
      this.showAuthModal = true;
      return;
    }

    this.addUserMessage(message);
    this.chatMessage = '';
    this.guestMessageCount++;

    this.addAssistantMessage(
      'Please log in or sign up to continue chatting with your investment advisor.'
    );

    this.saveDashboardState();
    return;
  }

  this.addUserMessage(message);
  this.chatMessage = '';

  this.isChatLoading = true;
  this.errorMessage = '';

  const request = {
    conversation_id: this.conversationId,
    message: message,

    investment_goal: this.investmentGoal,

    investment_amount:
      Number(this.investmentAmount),

    duration_years:
      Number(this.durationYears),

    risk_profile:
      this.data?.risk_profile || null,

    portfolio:
      this.data?.portfolio || null
  };

  this.apiService.sendChatMessage(request).subscribe(
    response => {

      this.conversationId =
        response.conversation_id;

      this.addAssistantMessage(
        response.message
      );

      // ======================================================
      // PORTFOLIO WAS UPDATED BY CHAT
      // ======================================================

      if (
        response.portfolio_updated &&
        response.updated_analysis
      ) {
        const updated =
          response.updated_analysis;

        this.data = {
          ...this.data,

          risk_profile:
            updated.risk_profile,

          portfolio:
            updated.portfolio,

          recommendations:
            updated.recommendations,

          critique:
            updated.critique,

          workflow_history:
            updated.workflow_history
        };

        this.investmentGoal =
          updated.investment_goal;

        this.investmentAmount =
          Number(updated.investment_amount);

        this.durationYears =
          Number(updated.duration_years);

        this.submitted = true;

        this.saveDashboardState();
      } else {
        // Save conversation even when the portfolio
        // was not changed.
        this.saveDashboardState();
      }

      this.isChatLoading = false;
    },

    error => {
      this.isChatLoading = false;

      this.errorMessage =
        error.error && error.error.detail
          ? error.error.detail
          : 'Unable to send your message. Please try again.';

      this.addAssistantMessage(
        'I was unable to process that message. Please try again.'
      );

      this.saveDashboardState();
    }
  );
}

  addUserMessage(message: string): void {

    this.chatMessages.push({
      role: 'user',
      content: message
    });
  }

  addAssistantMessage(message: string): void {

    this.chatMessages.push({
      role: 'assistant',
      content: message
    });
  }

  openAuthModal(): void {

    /*
     * Save before opening authentication.
     */
    this.saveDashboardState();

    this.showAuthModal = true;
  }

  closeAuthModal(): void {

    this.showAuthModal = false;
  }

  loginFromModal(): void {

    /*
     * VERY IMPORTANT:
     *
     * Save the portfolio before navigating away.
     */
    this.saveDashboardState();

    this.showAuthModal = false;

    this.router.navigate(
      ['/login'],
      {
        queryParams: {
          returnUrl: '/dashboard'
        }
      }
    );
  }

  signupFromModal(): void {

    /*
     * VERY IMPORTANT:
     *
     * Save the portfolio before navigating away.
     */
    this.saveDashboardState();

    this.showAuthModal = false;

    this.router.navigate(
      ['/signup'],
      {
        queryParams: {
          returnUrl: '/dashboard'
        }
      }
    );
  }

  allocationEntries():
    Array<{ name: string; amount: number }> {

    if (
      !this.data ||
      !this.data.portfolio
    ) {
      return [];
    }

    return Object.keys(
      this.data.portfolio
    ).map(name => ({

      name,

      amount:
        Number(
          this.data.portfolio[name]
        )
    }));
  }

  allocationTotal(): number {

    return this
      .allocationEntries()
      .reduce(
        (total, item) =>
          total + item.amount,
        0
      );
  }

  allocationPercent(
    amount: number
  ): number {

    const total =
      this.allocationTotal();

    return total
      ? (amount / total) * 100
      : 0;
  }

  getRecommendations(): any[] {

    if (
      !this.data ||
      !this.data.recommendations
    ) {
      return [];
    }

    return this.data.recommendations;
  }

  exportResults(): void {

    if (!this.data) {
      return;
    }

    const blob = new Blob(
      [
        JSON.stringify(
          this.data,
          null,
          2
        )
      ],
      {
        type: 'application/json'
      }
    );

    const url =
      window.URL.createObjectURL(blob);

    const link =
      document.createElement('a');

    link.href = url;

    link.download =
      'investment-analysis.json';

    link.click();

    window.URL.revokeObjectURL(url);
  }
}