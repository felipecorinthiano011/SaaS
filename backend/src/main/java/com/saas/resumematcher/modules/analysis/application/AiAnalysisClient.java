package com.saas.resumematcher.modules.analysis.application;

import com.saas.resumematcher.common.config.ApplicationProperties;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
@RequiredArgsConstructor
public class AiAnalysisClient {

  private final ApplicationProperties properties;

  public AiAnalyzeResponse analyze(String jobDescription, String resumeText) {
    RestClient client = RestClient.builder().baseUrl(properties.aiService().baseUrl()).build();

    return client
        .post()
        .uri("/api/v1/analyze")
        .contentType(MediaType.APPLICATION_JSON)
        .body(new AiAnalyzeRequest(jobDescription, resumeText))
        .retrieve()
        .body(AiAnalyzeResponse.class);
  }

  public record AiAnalyzeRequest(String jobDescription, String resumeText) {}

  public record AiAnalyzeResponse(
      Integer atsScore, List<String> extractedKeywords, String optimizedResume, String gapSummary) {}
}

