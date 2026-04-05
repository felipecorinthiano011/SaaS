package com.saas.resumematcher.modules.resume.application;

import jakarta.validation.constraints.NotBlank;
import java.time.Instant;

public final class ResumeDtos {

  private ResumeDtos() {}

  public record UploadRequest(@NotBlank String fileName, @NotBlank String extractedText) {}

  public record UploadResponse(
      Long id, String fileName, String userEmail, Instant uploadedAt, String message) {}

  public record ResumeDetailResponse(
      Long id, String fileName, String userEmail, String extractedText, Instant uploadedAt) {}
}

