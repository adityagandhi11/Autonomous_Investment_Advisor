import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { SignupRequest } from '../../models/auth';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {

  name = '';
  email = '';
  password = '';
  confirmPassword = '';

  errorMessage = '';
  isLoading = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  signup(): void {

    this.errorMessage = '';

    if (
      !this.name ||
      !this.email ||
      !this.password ||
      !this.confirmPassword
    ) {
      this.errorMessage = 'Please fill in all fields.';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match.';
      return;
    }

    if (this.password.length < 8) {
      this.errorMessage =
        'Password must contain at least 8 characters.';
      return;
    }

    const request: SignupRequest = {
      name: this.name,
      email: this.email,
      password: this.password
    };

    this.isLoading = true;

    this.authService.signup(request).subscribe({

      next: () => {
        this.isLoading = false;

        // Signup automatically logs the user in
        this.router.navigate(['/dashboard']);
      },

      error: (error) => {
        this.isLoading = false;

        this.errorMessage =
          error?.error?.detail ||
          'Unable to create your account.';
      }

    });
  }

  goToLogin(): void {
    this.router.navigate(['/login']);
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}