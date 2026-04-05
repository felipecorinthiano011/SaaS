package com.saas.resumematcher.modules.resume.api;

import com.saas.resumematcher.modules.resume.application.ResumeDtos;
import com.saas.resumematcher.modules.resume.application.ResumeService;
import com.saas.resumematcher.modules.resume.infra.AiTextExtractClient;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/resume")
@RequiredArgsConstructor
public class ResumeController {

  private final ResumeService resumeService;
  private final AiTextExtractClient aiTextExtractClient;

  @PostMapping("/upload")
  public ResponseEntity<ResumeDtos.UploadResponse> uploadResume(
      Authentication authentication,
      @RequestParam("file") MultipartFile file)
      throws IOException {
    String userEmail = authentication.getName();
    String mimeType = file.getContentType() != null ? file.getContentType() : "application/octet-stream";
    byte[] fileBytes = file.getBytes();

    // Call AI service to extract text from the file (falls back to "" if unavailable)
    String extractedText = aiTextExtractClient.extractText(fileBytes, file.getOriginalFilename());

    ResumeDtos.UploadResponse response =
        resumeService.uploadResume(
            userEmail,
            new ResumeDtos.UploadRequest(file.getOriginalFilename(), extractedText),
            fileBytes,
            mimeType);

    return ResponseEntity.ok(response);
  }

  @GetMapping("/{id}")
  public ResponseEntity<ResumeDtos.ResumeDetailResponse> getResume(
      @PathVariable Long id, Authentication authentication) {
    ResumeDtos.ResumeDetailResponse response =
        resumeService.getResume(id, authentication.getName());
    return ResponseEntity.ok(response);
  }

  @GetMapping
  public ResponseEntity<List<ResumeDtos.ResumeDetailResponse>> listResumes(
      Authentication authentication) {
    List<ResumeDtos.ResumeDetailResponse> resumes =
        resumeService.listResumes(authentication.getName());
    return ResponseEntity.ok(resumes);
  }
}

