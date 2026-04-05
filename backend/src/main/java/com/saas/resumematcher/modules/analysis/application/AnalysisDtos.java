package com.saas.resumematcher.modules.analysis.application;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import java.time.Instant;
import java.util.List;

public final class AnalysisDtos {

  private AnalysisDtos() {}

  public record AnalyzeRequest(
      @NotBlank String jobDescription,
      @NotBlank String resumeText,
      @Min(1) Long resumeId) {}

  public record AnalyzeResponse(
      Long id,
      Long resumeId,
      Integer atsScore,
      List<String> extractedKeywords,
      String optimizedResume,
      String gapSummary,
      Instant createdAt) {}
}
