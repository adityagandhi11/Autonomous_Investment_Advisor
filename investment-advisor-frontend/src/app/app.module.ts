import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app.routes';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { RiskAnalyticsComponent } from './components/risk-analytics/risk-analytics.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    RiskAnalyticsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}