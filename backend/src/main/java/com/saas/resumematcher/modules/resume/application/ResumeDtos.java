package com.saas.resumematcher.modules.resume.application;

import java.time.Instant;

public final class ResumeDtos {

  private ResumeDtos() {}

  public record UploadRequest(String fileName, String extractedText) {}

  public record UploadResponse(
      Long id, String fileName, String userEmail, Instant uploadedAt, String message, String text) {}

  public record ResumeDetailResponse(
      Long id, String fileName, String userEmail, String extractedText, Instant uploadedAt) {}
}

