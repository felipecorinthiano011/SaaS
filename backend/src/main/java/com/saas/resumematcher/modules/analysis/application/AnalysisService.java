package com.saas.resumematcher.modules.analysis.application;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.saas.resumematcher.modules.analysis.domain.ResumeAnalysisEntity;
import com.saas.resumematcher.modules.analysis.infra.ResumeAnalysisRepository;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AnalysisService {

  private final AiAnalysisClient aiAnalysisClient;
  private final ResumeAnalysisRepository resumeAnalysisRepository;
  private final ObjectMapper objectMapper = new ObjectMapper();

  @Transactional
  public AnalysisDtos.AnalyzeResponse analyzeResume(
      String userEmail, AnalysisDtos.AnalyzeRequest request) {
    AiAnalysisClient.AiAnalyzeResponse aiResponse =
        aiAnalysisClient.analyze(request.jobDescription(), request.resumeText());

    List<String> flatKeywords = flattenKeywords(aiResponse.extractedKeywords());
    List<String> missing = aiResponse.missingKeywords() != null ? aiResponse.missingKeywords() : List.of();
    List<AiAnalysisClient.SuggestionData> rawSuggestions =
        aiResponse.suggestions() != null ? aiResponse.suggestions() : List.of();

    ResumeAnalysisEntity entity =
        ResumeAnalysisEntity.builder()
            .userEmail(userEmail)
            .resumeId(request.resumeId())
            .jobDescription(request.jobDescription())
            .resumeText(request.resumeText())
            .atsScore(aiResponse.atsScore())
            .extractedKeywords(writeJson(flatKeywords))
            .missingKeywords(writeJson(missing))
            .suggestionsJson(writeSuggestionsJson(rawSuggestions))
            .optimizedResume(aiResponse.optimizedResume())
            .gapSummary(aiResponse.gapSummary())
            .createdAt(Instant.now())
            .build();

    ResumeAnalysisEntity saved = resumeAnalysisRepository.save(entity);
    return map(saved, flatKeywords, missing, toSuggestionDtos(rawSuggestions));
  }

  @Transactional(readOnly = true)
  public AnalysisDtos.AnalyzeResponse getAnalysis(Long id, String userEmail) {
    ResumeAnalysisEntity entity =
        resumeAnalysisRepository
            .findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Analysis not found"));

    if (!entity.getUserEmail().equals(userEmail)) {
      throw new IllegalArgumentException("Unauthorized access to analysis");
    }

    return map(
        entity,
        readKeywords(entity.getExtractedKeywords()),
        readKeywords(entity.getMissingKeywords()),
        readSuggestions(entity.getSuggestionsJson()));
  }

  @Transactional(readOnly = true)
  public List<AnalysisDtos.AnalyzeResponse> listAnalyses(String userEmail) {
    return resumeAnalysisRepository.findAllByUserEmailOrderByCreatedAtDesc(userEmail).stream()
        .map(entity -> map(
            entity,
            readKeywords(entity.getExtractedKeywords()),
            readKeywords(entity.getMissingKeywords()),
            readSuggestions(entity.getSuggestionsJson())))
        .toList();
  }

  private AnalysisDtos.AnalyzeResponse map(
      ResumeAnalysisEntity entity, List<String> keywords, List<String> missing,
      List<AnalysisDtos.SuggestionDto> suggestions) {
    return new AnalysisDtos.AnalyzeResponse(
        entity.getId(),
        entity.getResumeId(),
        entity.getAtsScore(),
        keywords,
        missing,
        entity.getOptimizedResume(),
        entity.getGapSummary(),
        suggestions,
        entity.getCreatedAt());
  }

  /** Flatten the AI service's KeywordsData object into a single list of strings. */
  private List<String> flattenKeywords(AiAnalysisClient.KeywordsData data) {
    if (data == null) return List.of();
    List<String> all = new ArrayList<>();
    if (data.technical_keywords() != null) all.addAll(data.technical_keywords());
    if (data.soft_skills() != null) all.addAll(data.soft_skills());
    if (data.certifications() != null) all.addAll(data.certifications());
    if (data.required_experience() != null) all.addAll(data.required_experience());
    return all;
  }

  private List<AnalysisDtos.SuggestionDto> toSuggestionDtos(
      List<AiAnalysisClient.SuggestionData> raw) {
    if (raw == null) return List.of();
    return raw.stream()
        .map(s -> new AnalysisDtos.SuggestionDto(s.category(), s.suggestion(), s.priority(), s.impact()))
        .toList();
  }

  private String writeJson(List<String> keywords) {
    try {
      return objectMapper.writeValueAsString(keywords);
    } catch (JsonProcessingException ex) {
      throw new IllegalStateException("Failed to serialize keywords", ex);
    }
  }

  private String writeSuggestionsJson(List<AiAnalysisClient.SuggestionData> suggestions) {
    try {
      return objectMapper.writeValueAsString(suggestions);
    } catch (JsonProcessingException ex) {
      return "[]";
    }
  }

  private List<String> readKeywords(String keywordsJson) {
    if (keywordsJson == null || keywordsJson.isBlank()) return List.of();
    try {
      return objectMapper.readerForListOf(String.class).readValue(keywordsJson);
    } catch (JsonProcessingException ex) {
      return List.of();
    }
  }

  private List<AnalysisDtos.SuggestionDto> readSuggestions(String json) {
    if (json == null || json.isBlank()) return List.of();
    try {
      return objectMapper.readerForListOf(AnalysisDtos.SuggestionDto.class).readValue(json);
    } catch (JsonProcessingException ex) {
      return List.of();
    }
  }
}
