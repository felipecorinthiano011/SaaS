package com.saas.resumematcher.modules.analysis.application;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.saas.resumematcher.modules.analysis.domain.ResumeAnalysisEntity;
import com.saas.resumematcher.modules.analysis.infra.ResumeAnalysisRepository;
import java.time.Instant;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AnalysisService {

  private final AiAnalysisClient aiAnalysisClient;
  private final ResumeAnalysisRepository resumeAnalysisRepository;
  private final ObjectMapper objectMapper = new ObjectMapper();

  public AnalysisDtos.AnalyzeResponse analyzeResume(
      String userEmail, AnalysisDtos.AnalyzeRequest request) {
    AiAnalysisClient.AiAnalyzeResponse aiResponse =
        aiAnalysisClient.analyze(request.jobDescription(), request.resumeText());

    ResumeAnalysisEntity entity =
        ResumeAnalysisEntity.builder()
            .userEmail(userEmail)
            .jobDescription(request.jobDescription())
            .resumeText(request.resumeText())
            .atsScore(aiResponse.atsScore())
            .extractedKeywords(writeJson(aiResponse.extractedKeywords()))
            .optimizedResume(aiResponse.optimizedResume())
            .gapSummary(aiResponse.gapSummary())
            .createdAt(Instant.now())
            .build();

    ResumeAnalysisEntity saved = resumeAnalysisRepository.save(entity);
    return map(saved, aiResponse.extractedKeywords());
  }

  public List<AnalysisDtos.AnalyzeResponse> listAnalyses(String userEmail) {
    return resumeAnalysisRepository.findAllByUserEmailOrderByCreatedAtDesc(userEmail).stream()
        .map(entity -> map(entity, readKeywords(entity.getExtractedKeywords())))
        .toList();
  }

  private AnalysisDtos.AnalyzeResponse map(ResumeAnalysisEntity entity, List<String> keywords) {
    return new AnalysisDtos.AnalyzeResponse(
        entity.getId(),
        entity.getAtsScore(),
        keywords,
        entity.getOptimizedResume(),
        entity.getGapSummary(),
        entity.getCreatedAt());
  }

  private String writeJson(List<String> keywords) {
    try {
      return objectMapper.writeValueAsString(keywords);
    } catch (JsonProcessingException ex) {
      throw new IllegalStateException("Failed to serialize keywords", ex);
    }
  }

  private List<String> readKeywords(String keywordsJson) {
    try {
      return objectMapper.readerForListOf(String.class).readValue(keywordsJson);
    } catch (JsonProcessingException ex) {
      throw new IllegalStateException("Failed to deserialize keywords", ex);
    }
  }
}

