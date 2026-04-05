package com.saas.resumematcher.modules.resume.application;

import com.saas.resumematcher.modules.resume.domain.ResumeEntity;
import com.saas.resumematcher.modules.resume.infra.ResumeRepository;
import java.time.Instant;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ResumeService {

  private final ResumeRepository resumeRepository;

  public ResumeDtos.UploadResponse uploadResume(
      String userEmail, ResumeDtos.UploadRequest request, byte[] fileContent, String mimeType) {
    ResumeEntity entity =
        ResumeEntity.builder()
            .userEmail(userEmail)
            .fileName(request.fileName())
            .extractedText(request.extractedText())
            .fileContent(fileContent)
            .mimeType(mimeType)
            .uploadedAt(Instant.now())
            .createdAt(Instant.now())
            .build();

    ResumeEntity saved = resumeRepository.save(entity);
    return new ResumeDtos.UploadResponse(
        saved.getId(),
        saved.getFileName(),
        saved.getUserEmail(),
        saved.getUploadedAt(),
        "Resume uploaded successfully");
  }

  public ResumeDtos.ResumeDetailResponse getResume(Long resumeId, String userEmail) {
    ResumeEntity resume = resumeRepository.findById(resumeId)
        .orElseThrow(() -> new IllegalArgumentException("Resume not found"));

    if (!resume.getUserEmail().equals(userEmail)) {
      throw new IllegalArgumentException("Unauthorized access to resume");
    }

    return new ResumeDtos.ResumeDetailResponse(
        resume.getId(),
        resume.getFileName(),
        resume.getUserEmail(),
        resume.getExtractedText(),
        resume.getUploadedAt());
  }

  public List<ResumeDtos.ResumeDetailResponse> listResumes(String userEmail) {
    return resumeRepository.findAllByUserEmailOrderByUploadedAtDesc(userEmail).stream()
        .map(
            resume ->
                new ResumeDtos.ResumeDetailResponse(
                    resume.getId(),
                    resume.getFileName(),
                    resume.getUserEmail(),
                    resume.getExtractedText(),
                    resume.getUploadedAt()))
        .toList();
  }

  public String getLatestResumeText(String userEmail) {
    return resumeRepository
        .findLatestByUserEmail(userEmail)
        .map(ResumeEntity::getExtractedText)
        .orElse("");
  }
}

