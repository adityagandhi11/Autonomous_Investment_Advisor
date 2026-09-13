import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { SignupRequest } from '../../models/auth';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  name = '';
  email = '';
  password = '';
  confirmPassword = '';

  errorMessage = '';
  isLoading = false;

  returnUrl = '/dashboard';

  constructor(
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {

    /*
     * Read the destination that sent the user
     * to Signup.
     */
    this.route.queryParams.subscribe(params => {

      if (params['returnUrl']) {
        this.returnUrl = params['returnUrl'];
      }

    });
  }

  signup(): void {

    this.errorMessage = '';

    if (
      !this.name ||
      !this.email ||
      !this.password ||
      !this.confirmPassword
    ) {

      this.errorMessage =
        'Please fill in all fields.';

      return;
    }

    if (
      this.password !== this.confirmPassword
    ) {

      this.errorMessage =
        'Passwords do not match.';

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

    this.authService
      .signup(request)
      .subscribe({

        next: () => {

          this.isLoading = false;

          /*
           * Signup automatically authenticates
           * the user through AuthService.
           *
           * Return to the original destination.
           */
          this.router.navigateByUrl(
            this.returnUrl
          );
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

    this.router.navigate(
      ['/login'],
      {
        queryParams: {
          returnUrl: this.returnUrl
        }
      }
    );
  }

  goToDashboard(): void {

    this.router.navigate(['/dashboard']);
  }
}