import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { LoginRequest } from '../../models/auth';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  email = '';
  password = '';

  errorMessage = '';
  isLoading = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  login(): void {

    this.errorMessage = '';

    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter your email and password.';
      return;
    }

    const request: LoginRequest = {
      email: this.email,
      password: this.password
    };

    this.isLoading = true;

    this.authService.login(request).subscribe({

      next: () => {
        this.isLoading = false;

        // Return to the dashboard after successful login
        this.router.navigate(['/dashboard']);
      },

      error: (error) => {
        this.isLoading = false;

        this.errorMessage =
          error?.error?.detail ||
          'Login failed. Please check your credentials.';
      }

    });
  }

  goToSignup(): void {
    this.router.navigate(['/signup']);
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}