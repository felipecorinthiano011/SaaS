import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';

export interface AnalyzeResumeRequest {
  jobDescription: string;
  resumeText: string;
}

export interface AnalyzeResumeResponse {
  atsScore: number;
  extractedKeywords: string[];
  optimizedResume: string;
  gapSummary: string;
}

@Injectable({ providedIn: 'root' })
export class AnalysisApiService {
  constructor(private readonly http: HttpClient) {}

  analyzeResume(payload: AnalyzeResumeRequest): Observable<AnalyzeResumeResponse> {
    return this.http.post<AnalyzeResumeResponse>(`${environment.apiBaseUrl}/analysis`, payload);
  }
}

