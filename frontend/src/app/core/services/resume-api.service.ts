import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface AnalysisRequest {
  jobDescription: string;
  resumeText: string;
}

export interface Suggestion {
  category: string;
  suggestion: string;
  priority: 'high' | 'medium' | 'low';
  impact: string;
}

export interface OptimizeResumeResponse {
  id: number;
  resumeId: number | null;
  atsScore: number;
  extractedKeywords: string[];
  missingKeywords: string[];
  optimizedResume: string;
  gapSummary: string;
  suggestions: Suggestion[];
  createdAt: string;
}

export interface ExtractKeywordsResponse {
  skills: string[];
  technologies: string[];
  tools: string[];
  soft_skills: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ResumeApiService {
  private readonly BACKEND_URL = 'http://localhost:8080/api';
  private readonly AI_SERVICE_URL = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  /**
   * Upload resume file and extract text
   */
  uploadResume(file: File): Observable<{ text: string; filename: string }> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<{ text: string; filename: string }>(
      `${this.BACKEND_URL}/resume/upload`,
      formData
    );
  }

  /**
   * Extract keywords from job description
   */
  extractKeywords(jobDescription: string): Observable<ExtractKeywordsResponse> {
    return this.http.post<ExtractKeywordsResponse>(
      `${this.AI_SERVICE_URL}/keywords/extract`,
      { job_description: jobDescription }
    );
  }

  /**
   * Optimize resume to match job description
   */
  optimizeResume(jobDescription: string, resumeText: string): Observable<OptimizeResumeResponse> {
    return this.http.post<OptimizeResumeResponse>(
      `${this.BACKEND_URL}/job/analyze`,
      {
        jobDescription,
        resumeText
      }
    );
  }

  /**
   * Get previous analysis results
   */
  getAnalysis(id: string): Observable<OptimizeResumeResponse> {
    return this.http.get<OptimizeResumeResponse>(
      `${this.BACKEND_URL}/job/${id}`
    );
  }

  /**
   * Get all analyses for current user
   */
  getAllAnalyses(): Observable<OptimizeResumeResponse[]> {
    return this.http.get<OptimizeResumeResponse[]>(
      `${this.BACKEND_URL}/job`
    );
  }
}

