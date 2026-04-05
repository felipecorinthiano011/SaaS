import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { ResumeApiService, OptimizeResumeResponse } from '../../core/services/resume-api.service';
import { AuthService } from '../../core/services';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  // Form inputs
  jobDescription = '';
  resumeText = '';
  selectedFile: File | null = null;

  // State
  isLoading = false;
  isUploading = false;
  errorMessage = '';
  successMessage = '';
  analysis: OptimizeResumeResponse | null = null;
  currentUserEmail = '';

  // UI state
  activeTab: 'input' | 'results' = 'input';
  showOptimizedResume = false;

  constructor(
    private resumeApiService: ResumeApiService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Get current user
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.currentUserEmail = user.email;
      }
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file && (file.type === 'application/pdf' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      this.selectedFile = file;
      this.errorMessage = '';

      // Extract text from file
      this.isUploading = true;
      this.resumeApiService.uploadResume(file).subscribe({
        next: (response) => {
          this.resumeText = response.text;
          this.successMessage = 'Resume uploaded successfully!';
          this.isUploading = false;
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage = 'Failed to upload resume. Please try again.';
          this.isUploading = false;
        }
      });
    } else {
      this.errorMessage = 'Please select a PDF or DOCX file';
    }
  }

  onAnalyze(): void {
    if (!this.jobDescription.trim()) {
      this.errorMessage = 'Please paste a job description';
      return;
    }

    if (!this.resumeText.trim()) {
      this.errorMessage = 'Please upload or paste your resume';
      return;
    }

    this.errorMessage = '';
    this.successMessage = '';
    this.isLoading = true;

    this.resumeApiService.optimizeResume(this.jobDescription, this.resumeText)
      .subscribe({
        next: (response) => {
          this.analysis = response;
          this.activeTab = 'results';
          this.isLoading = false;
          this.successMessage = 'Analysis completed successfully!';
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage = error.error?.message || 'Analysis failed. Please try again.';
          this.isLoading = false;
        }
      });
  }

  downloadOptimizedResume(): void {
    if (!this.analysis) return;

    const element = document.createElement('a');
    const file = new Blob([this.analysis.optimizedResume], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'optimized-resume.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }

  copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(() => {
      this.successMessage = 'Copied to clipboard!';
      setTimeout(() => this.successMessage = '', 2000);
    });
  }

  getAtsScoreColor(): string {
    if (!this.analysis) return 'gray';
    const score = this.analysis.atsScore;
    if (score >= 80) return 'green';
    if (score >= 60) return 'yellow';
    if (score >= 40) return 'orange';
    return 'red';
  }

  getAtsScoreText(): string {
    if (!this.analysis) return 'N/A';
    const score = this.analysis.atsScore;
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  resetForm(): void {
    this.jobDescription = '';
    this.resumeText = '';
    this.selectedFile = null;
    this.analysis = null;
    this.errorMessage = '';
    this.successMessage = '';
    this.activeTab = 'input';
  }
}
