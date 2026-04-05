package com.saas.resumematcher.modules.analysis.api;

import com.saas.resumematcher.modules.analysis.application.AnalysisDtos;
import com.saas.resumematcher.modules.analysis.application.AnalysisService;
import jakarta.validation.Valid;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/analysis")
@RequiredArgsConstructor
public class AnalysisController {

  private final AnalysisService analysisService;

  @PostMapping
  public AnalysisDtos.AnalyzeResponse analyze(
      Authentication authentication, @Valid @RequestBody AnalysisDtos.AnalyzeRequest request) {
    return analysisService.analyzeResume(authentication.getName(), request);
  }

  @GetMapping
  public List<AnalysisDtos.AnalyzeResponse> list(Authentication authentication) {
    return analysisService.listAnalyses(authentication.getName());
  }
}

