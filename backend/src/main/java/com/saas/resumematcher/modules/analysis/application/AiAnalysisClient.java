package com.saas.resumematcher.modules.analysis.application;

import com.saas.resumematcher.common.config.ApplicationProperties;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
@RequiredArgsConstructor
public class AiAnalysisClient {

  private final ApplicationProperties properties;

  public AiAnalyzeResponse analyze(String jobDescription, String resumeText) {
    RestTemplate restTemplate = new RestTemplate();

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    HttpEntity<AiAnalyzeRequest> entity =
        new HttpEntity<>(new AiAnalyzeRequest(jobDescription, resumeText), headers);

    return restTemplate.postForObject(
        properties.aiService().baseUrl() + "/api/v1/analyze",
        entity,
        AiAnalyzeResponse.class);
  }

  /** Typed request body for the AI service. */
  public record AiAnalyzeRequest(String jobDescription, String resumeText) {}

  // Matches the actual KeywordsData object returned by the AI service
  public record KeywordsData(
      List<String> technical_keywords,
      List<String> soft_skills,
      List<String> certifications,
      List<String> required_experience) {}

  // Matches the Suggestion object returned by the AI service
  public record SuggestionData(
      String category,
      String suggestion,
      String priority,
      String impact) {}

  public record AiAnalyzeResponse(
      Integer atsScore,
      KeywordsData extractedKeywords,
      List<String> matchedKeywords,
      List<String> missingKeywords,
      String optimizedResume,
      List<SuggestionData> suggestions,
      String gapSummary) {}
}

