import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { LoginRequest } from '../../models/auth';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  email = '';
  password = '';

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
     * Read the destination that sent the user to Login.
     *
     * Example:
     *
     * /login?returnUrl=/dashboard
     */
    this.route.queryParams.subscribe(params => {

      if (params['returnUrl']) {
        this.returnUrl = params['returnUrl'];
      }

    });
  }

  login(): void {

    this.errorMessage = '';

    if (!this.email || !this.password) {

      this.errorMessage =
        'Please enter your email and password.';

      return;
    }

    const request: LoginRequest = {

      email: this.email,

      password: this.password
    };

    this.isLoading = true;

    this.authService
      .login(request)
      .subscribe({

        next: () => {

          this.isLoading = false;

          /*
           * AuthService has already stored the JWT
           * and user information.
           *
           * Now return to the page that initiated
           * authentication.
           */
          this.router.navigateByUrl(
            this.returnUrl
          );
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

    this.router.navigate(
      ['/signup'],
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