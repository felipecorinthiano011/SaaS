package com.saas.resumematcher.modules.analysis.api;

import com.saas.resumematcher.modules.analysis.application.AnalysisDtos;
import com.saas.resumematcher.modules.analysis.application.AnalysisService;
import jakarta.validation.Valid;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/job")
@RequiredArgsConstructor
public class AnalysisController {

  private final AnalysisService analysisService;

  @PostMapping("/analyze")
  public ResponseEntity<AnalysisDtos.AnalyzeResponse> analyze(
      Authentication authentication, @Valid @RequestBody AnalysisDtos.AnalyzeRequest request) {
    AnalysisDtos.AnalyzeResponse response =
        analysisService.analyzeResume(authentication.getName(), request);
    return ResponseEntity.ok(response);
  }

  @GetMapping("/{id}")
  public ResponseEntity<AnalysisDtos.AnalyzeResponse> getAnalysis(
      @PathVariable Long id, Authentication authentication) {
    AnalysisDtos.AnalyzeResponse response =
        analysisService.getAnalysis(id, authentication.getName());
    return ResponseEntity.ok(response);
  }

  @GetMapping
  public List<AnalysisDtos.AnalyzeResponse> list(Authentication authentication) {
    return analysisService.listAnalyses(authentication.getName());
  }
}
