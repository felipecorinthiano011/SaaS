import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgFor, NgIf } from '@angular/common';

import {
  AnalysisApiService,
  AnalyzeResumeResponse
} from '../../core/services/analysis-api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [FormsModule, NgIf, NgFor],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent {
  jobDescription = '';
  resumeText = '';
  analysis: AnalyzeResumeResponse | null = null;
  isLoading = false;
  errorMessage = '';

  constructor(private readonly analysisApiService: AnalysisApiService) {}

  submit(): void {
    this.errorMessage = '';
    this.isLoading = true;
    this.analysis = null;

    this.analysisApiService
      .analyzeResume({
        jobDescription: this.jobDescription,
        resumeText: this.resumeText
      })
      .subscribe({
        next: (response) => {
          this.analysis = response;
          this.isLoading = false;
        },
        error: () => {
          this.errorMessage = 'Analysis request failed. Please try again.';
          this.isLoading = false;
        }
      });
  }
}

