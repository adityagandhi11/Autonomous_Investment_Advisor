// import { Component, OnInit } from '@angular/core';
// import { Router } from '@angular/router';

// import { ApiService, InvestmentRequest } from '../../services/api.service';
// import { AuthService } from '../../services/auth.service';
// import { User } from '../../models/auth';

// @Component({
//   selector: 'app-dashboard',
//   templateUrl: './dashboard.component.html',
//   styleUrls: ['./dashboard.component.css']
// })
// export class DashboardComponent implements OnInit {

//   data: any;

//   investmentGoal = 'I want to invest for long-term wealth creation';
//   investmentAmount = 50000;
//   durationYears = 5;

//   isLoading = false;
//   errorMessage = '';
//   submitted = false;

//   // ============================================================
//   // AUTHENTICATION
//   // ============================================================

//   currentUser: User | null = null;
//   isAuthenticated = false;

//   // ============================================================
//   // CHAT
//   // ============================================================

//   chatMessage = '';
//   chatMessages: Array<{
//     role: 'user' | 'assistant';
//     content: string;
//   }> = [];

//   guestMessageCount = 0;

//   showAuthModal = false;

//   constructor(
//     private apiService: ApiService,
//     private authService: AuthService,
//     private router: Router
//   ) {}

//   ngOnInit(): void {
//     this.fetchData();
//     this.loadAuthenticationState();
//   }

//   // ============================================================
//   // AUTHENTICATION
//   // ============================================================

//   loadAuthenticationState(): void {
//     this.isAuthenticated = this.authService.isAuthenticated();
//     this.currentUser = this.authService.getUser();
//   }

//   goToLogin(): void {
//     this.router.navigate(['/login']);
//   }

//   goToSignup(): void {
//     this.router.navigate(['/signup']);
//   }

//   logout(): void {
//     this.authService.logout();

//     this.isAuthenticated = false;
//     this.currentUser = null;

//     this.chatMessages = [];
//     this.guestMessageCount = 0;
//   }

//   // ============================================================
//   // EXISTING DASHBOARD FUNCTIONALITY
//   // ============================================================

//   fetchData(): void {
//     this.data = undefined;
//     this.submitted = false;
//     this.errorMessage = '';
//   }

//   analyzePortfolio(): void {

//     if (
//       !this.investmentGoal.trim() ||
//       this.investmentAmount < 1000 ||
//       this.durationYears < 1
//     ) {
//       this.errorMessage =
//         'Enter a goal, an amount of at least ₹1,000, and a valid horizon.';

//       return;
//     }

//     const request: InvestmentRequest = {
//       user_goal: this.investmentGoal.trim(),
//       investment_amount: Number(this.investmentAmount),
//       duration_years: Number(this.durationYears)
//     };

//     this.isLoading = true;
//     this.submitted = true;
//     this.errorMessage = '';

//     this.apiService.analyzeInvestment(request).subscribe(
//       response => {

//         this.data = response;
//         this.isLoading = false;

//       },
//       error => {

//         this.isLoading = false;

//         this.errorMessage =
//           error.error && error.error.detail
//             ? error.error.detail
//             : 'Unable to complete the analysis. Check that FastAPI is running on port 8000.';
//       }
//     );
//   }

//   // ============================================================
//   // CHAT
//   // ============================================================

//   sendChatMessage(): void {

//     const message = this.chatMessage.trim();

//     if (!message) {
//       return;
//     }

//     /*
//      * Authenticated users can continue chatting.
//      */
//     if (this.isAuthenticated) {

//       this.addUserMessage(message);

//       this.chatMessage = '';

//       /*
//        * Chat backend will be connected in the next backend step.
//        */
//       this.addAssistantMessage(
//         'I’m ready to help with your investment question. The authenticated chat service will be connected next.'
//       );

//       return;
//     }

//     /*
//      * Guest users get exactly one free message.
//      */
//     if (this.guestMessageCount >= 1) {

//       this.showAuthModal = true;

//       return;
//     }

//     this.addUserMessage(message);

//     this.chatMessage = '';

//     this.guestMessageCount++;

//     /*
//      * Temporary response until the conversational backend
//      * is connected.
//      */
//     this.addAssistantMessage(
//       'Thanks for your question. I can help you build and understand an investment strategy.'
//     );
//   }

//   addUserMessage(message: string): void {

//     this.chatMessages.push({
//       role: 'user',
//       content: message
//     });
//   }

//   addAssistantMessage(message: string): void {

//     this.chatMessages.push({
//       role: 'assistant',
//       content: message
//     });
//   }

//   openAuthModal(): void {
//     this.showAuthModal = true;
//   }

//   closeAuthModal(): void {
//     this.showAuthModal = false;
//   }

//   loginFromModal(): void {

//     this.showAuthModal = false;

//     this.router.navigate(['/login']);
//   }

//   signupFromModal(): void {

//     this.showAuthModal = false;

//     this.router.navigate(['/signup']);
//   }

//   // ============================================================
//   // EXISTING RESULT FUNCTIONS
//   // ============================================================

//   allocationEntries(): Array<{ name: string; amount: number }> {

//     if (!this.data || !this.data.portfolio) {
//       return [];
//     }

//     return Object.keys(this.data.portfolio).map(name => ({
//       name,
//       amount: Number(this.data.portfolio[name])
//     }));
//   }

//   allocationTotal(): number {

//     return this.allocationEntries()
//       .reduce(
//         (total, item) => total + item.amount,
//         0
//       );
//   }

//   allocationPercent(amount: number): number {

//     const total = this.allocationTotal();

//     return total
//       ? (amount / total) * 100
//       : 0;
//   }

//   getRecommendations(): any[] {

//     if (!this.data || !this.data.recommendations) {
//       return [];
//     }

//     return this.data.recommendations;
//   }

//   exportResults(): void {

//     if (!this.data) {
//       return;
//     }

//     const blob = new Blob(
//       [
//         JSON.stringify(
//           this.data,
//           null,
//           2
//         )
//       ],
//       {
//         type: 'application/json'
//       }
//     );

//     const url = window.URL.createObjectURL(blob);

//     const link = document.createElement('a');

//     link.href = url;
//     link.download = 'investment-analysis.json';

//     link.click();

//     window.URL.revokeObjectURL(url);
//   }
// }


import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ApiService, InvestmentRequest } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/auth';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  // ============================================================
  // EXISTING PORTFOLIO DATA
  // ============================================================

  data: any;

  investmentGoal = 'I want to invest for long-term wealth creation';
  investmentAmount = 50000;
  durationYears = 5;

  isLoading = false;
  errorMessage = '';
  submitted = false;

  // ============================================================
  // AUTHENTICATION
  // ============================================================

  currentUser: User | null = null;
  isAuthenticated = false;

  // ============================================================
  // CHAT
  // ============================================================

  conversationId: string | null = null;

  chatMessage = '';

  chatMessages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }> = [];

  /*
   * Number of chat messages sent by a guest user.
   *
   * Guest rule:
   * - First chat message -> allowed
   * - Second chat message -> login/signup modal
   *
   * Authenticated users have no guest restriction.
   */
  guestMessageCount = 0;

  showAuthModal = false;

  // ============================================================
  // CONSTRUCTOR
  // ============================================================

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router
  ) {}

  // ============================================================
  // LIFECYCLE
  // ============================================================

  ngOnInit(): void {
    this.fetchData();
    this.loadAuthenticationState();
  }

  // ============================================================
  // DASHBOARD STATE
  // ============================================================

  /**
   * Returns true after a portfolio analysis has completed
   * successfully.
   *
   * The dashboard HTML uses this to switch between:
   *
   * 1. Initial portfolio form
   * 2. Chat interface
   */
  get hasAnalysis(): boolean {
    return !!this.data;
  }

  // ============================================================
  // AUTHENTICATION
  // ============================================================

  loadAuthenticationState(): void {
    this.isAuthenticated = this.authService.isAuthenticated();
    this.currentUser = this.authService.getUser();
  }

  goToLogin(): void {
    this.router.navigate(['/login']);
  }

  goToSignup(): void {
    this.router.navigate(['/signup']);
  }

  logout(): void {
    this.authService.logout();

    this.isAuthenticated = false;
    this.currentUser = null;

    /*
     * Clear chat state when the user logs out.
     */
    this.chatMessages = [];
    this.chatMessage = '';
    this.guestMessageCount = 0;
    this.conversationId = null;
    this.showAuthModal = false;
  }

  // ============================================================
  // EXISTING DASHBOARD FUNCTIONALITY
  // ============================================================

  fetchData(): void {
    this.data = undefined;
    this.submitted = false;
    this.errorMessage = '';

    this.chatMessages = [];
    this.chatMessage = '';
    this.conversationId = null;
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
      user_goal: this.investmentGoal.trim(),
      investment_amount: Number(this.investmentAmount),
      duration_years: Number(this.durationYears)
    };

    this.isLoading = true;
    this.submitted = true;
    this.errorMessage = '';

    /*
     * Start a fresh conversation whenever a new
     * portfolio analysis is performed.
     */
    this.conversationId = null;
    this.chatMessages = [];

    this.apiService.analyzeInvestment(request).subscribe(
      response => {

        /*
         * Keep the existing investment analysis response.
         */
        this.data = response;

        this.isLoading = false;

        /*
         * Start the conversational advisor after
         * the portfolio has been successfully generated.
         */
        this.chatMessages = [
          {
            role: 'assistant',
            content:
              'Your portfolio is ready. You can ask me why I recommended an asset, how the portfolio works, or request changes such as increasing your investment amount, changing the investment horizon, or adjusting your risk level.'
          }
        ];
      },
      error => {

        this.isLoading = false;

        this.errorMessage =
          error.error && error.error.detail
            ? error.error.detail
            : 'Unable to complete the analysis. Check that FastAPI is running on port 8000.';
      }
    );
  }

  // ============================================================
  // CHAT
  // ============================================================

  /**
   * Send a chat message.
   *
   * Guest users:
   * - First message is allowed.
   * - Second message opens authentication modal.
   *
   * Authenticated users:
   * - Message is sent to the FastAPI /chat endpoint.
   * - conversation_id is reused for subsequent messages.
   */
  sendChatMessage(): void {

    const message = this.chatMessage.trim();

    if (!message) {
      return;
    }

    // ==========================================================
    // GUEST USER
    // ==========================================================

    if (!this.isAuthenticated) {

      /*
       * Guest has already used the free message.
       */
      if (this.guestMessageCount >= 1) {
        this.showAuthModal = true;
        return;
      }

      /*
       * Allow the first guest message.
       */
      this.addUserMessage(message);

      this.chatMessage = '';

      this.guestMessageCount++;

      /*
       * Temporary guest response.
       *
       * We will later decide whether guest messages should
       * also be processed by the backend.
       */
      this.addAssistantMessage(
        'Please log in or sign up to continue chatting with your investment advisor.'
      );

      return;
    }

    // ==========================================================
    // AUTHENTICATED USER
    // ==========================================================

    /*
     * Immediately display the user's message.
     */
    this.addUserMessage(message);

    this.chatMessage = '';

    this.isLoading = true;
    this.errorMessage = '';

    /*
     * Send the current investment context along with
     * the user's message.
     */
    const request = {
      conversation_id: this.conversationId,
      message: message,

      investment_goal: this.investmentGoal,
      investment_amount: Number(this.investmentAmount),
      duration_years: Number(this.durationYears),

      risk_profile: this.data?.risk_profile || null,
      portfolio: this.data?.portfolio || null
    };

    this.apiService.sendChatMessage(request).subscribe(
      response => {

        /*
         * Save the conversation ID returned by the backend.
         *
         * The next message will reuse this ID so that
         * MongoDB conversation history is maintained.
         */
        this.conversationId = response.conversation_id;

        /*
         * Display the actual LLM response.
         */
        this.addAssistantMessage(response.message);

        this.isLoading = false;
      },
      error => {

        this.isLoading = false;

        this.errorMessage =
          error.error && error.error.detail
            ? error.error.detail
            : 'Unable to send your message. Please try again.';

        this.addAssistantMessage(
          'I was unable to process that message. Please try again.'
        );
      }
    );
  }

  /**
   * Add a user message to the conversation.
   */
  addUserMessage(message: string): void {

    this.chatMessages.push({
      role: 'user',
      content: message
    });
  }

  /**
   * Add an assistant message to the conversation.
   */
  addAssistantMessage(message: string): void {

    this.chatMessages.push({
      role: 'assistant',
      content: message
    });
  }

  // ============================================================
  // AUTH MODAL
  // ============================================================

  openAuthModal(): void {
    this.showAuthModal = true;
  }

  closeAuthModal(): void {
    this.showAuthModal = false;
  }

  loginFromModal(): void {

    this.showAuthModal = false;

    this.router.navigate(['/login']);
  }

  signupFromModal(): void {

    this.showAuthModal = false;

    this.router.navigate(['/signup']);
  }

  // ============================================================
  // EXISTING RESULT FUNCTIONS
  // ============================================================

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

    return this.allocationEntries()
      .reduce(
        (total, item) => total + item.amount,
        0
      );
  }

  allocationPercent(amount: number): number {

    const total = this.allocationTotal();

    return total
      ? (amount / total) * 100
      : 0;
  }

  getRecommendations(): any[] {

    if (!this.data || !this.data.recommendations) {
      return [];
    }

    return this.data.recommendations;
  }

  // ============================================================
  // EXPORT
  // ============================================================

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

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');

    link.href = url;
    link.download = 'investment-analysis.json';

    link.click();

    window.URL.revokeObjectURL(url);
  }
}

