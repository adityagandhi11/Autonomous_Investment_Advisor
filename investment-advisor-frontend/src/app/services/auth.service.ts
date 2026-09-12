import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

import {
  SignupRequest,
  LoginRequest,
  AuthResponse,
  User
} from '../models/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly API_URL = 'http://127.0.0.1:8000';

  private readonly TOKEN_KEY = 'investment_advisor_token';
  private readonly USER_KEY = 'investment_advisor_user';

  constructor(private http: HttpClient) {}

  signup(request: SignupRequest): Observable<AuthResponse> {

    return this.http
      .post<AuthResponse>(
        `${this.API_URL}/auth/signup`,
        request
      )
      .pipe(
        tap(response => {
          this.storeAuthData(response);
        })
      );
  }

  login(request: LoginRequest): Observable<AuthResponse> {

    return this.http
      .post<AuthResponse>(
        `${this.API_URL}/auth/login`,
        request
      )
      .pipe(
        tap(response => {
          this.storeAuthData(response);
        })
      );
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getUser(): User | null {

    const user = localStorage.getItem(this.USER_KEY);

    if (!user) {
      return null;
    }

    try {
      return JSON.parse(user);
    } catch {
      return null;
    }
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  private storeAuthData(response: AuthResponse): void {

    localStorage.setItem(
      this.TOKEN_KEY,
      response.access_token
    );

    localStorage.setItem(
      this.USER_KEY,
      JSON.stringify(response.user)
    );
  }
}