// import { Component } from '@angular/core';

// @Component({
//   selector: 'app-root',
//   templateUrl: './app.component.html',
//   styleUrls: ['./app.component.css']
// })
// export class AppComponent {
//   title = 'Investment Advisor';
// }

import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

import { AuthService } from './services/auth.service';
import { User } from './models/auth';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  title = 'investment-advisor';

  currentUser: User | null = null;
  isAuthenticated = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {

    // Load authentication state when the application starts
    this.loadAuthenticationState();

    // Refresh authentication state whenever the route changes
    this.router.events.subscribe(event => {

      if (event instanceof NavigationEnd) {
        this.loadAuthenticationState();
      }

    });
  }

  /**
   * Load authentication information from AuthService.
   */
  private loadAuthenticationState(): void {

    this.isAuthenticated = this.authService.isAuthenticated();

    if (this.isAuthenticated) {
      this.currentUser = this.authService.getUser();
    } else {
      this.currentUser = null;
    }
  }

  /**
   * Navigate to Login page.
   */
  goToLogin(): void {

    this.router.navigate(
      ['/login'],
      {
        queryParams: {
          returnUrl: '/dashboard'
        }
      }
    );
  }

  /**
   * Navigate to Signup page.
   */
  goToSignup(): void {

    this.router.navigate(
      ['/signup'],
      {
        queryParams: {
          returnUrl: '/dashboard'
        }
      }
    );
  }

  /**
   * Logout the current user.
   */
  logout(): void {

    this.authService.logout();

    this.currentUser = null;
    this.isAuthenticated = false;

    // Dashboard is public, so send the user back there.
    this.router.navigate(['/dashboard']);
  }

  /**
   * Generate initials for the logged-in user's avatar.
   *
   * Example:
   * Aditya Gandhi -> AG
   * Aditya -> A
   */
  getUserInitials(): string {

    if (!this.currentUser || !this.currentUser.name) {
      return 'U';
    }

    const nameParts = this.currentUser.name
      .trim()
      .split(/\s+/);

    if (nameParts.length === 1) {
      return nameParts[0]
        .charAt(0)
        .toUpperCase();
    }

    return (
      nameParts[0].charAt(0) +
      nameParts[nameParts.length - 1].charAt(0)
    ).toUpperCase();
  }
}