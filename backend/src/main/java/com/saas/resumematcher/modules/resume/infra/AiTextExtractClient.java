package com.saas.resumematcher.modules.resume.infra;

import com.saas.resumematcher.common.config.ApplicationProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Slf4j
@Component
@RequiredArgsConstructor
public class AiTextExtractClient {

  private final ApplicationProperties properties;

  private record ExtractTextResponse(String text, String filename) {}

  /**
   * Send a file to the AI service for text extraction.
   *
   * @param fileBytes  raw file bytes
   * @param filename   original file name (used to detect format)
   * @return extracted text, or empty string if the AI service is unavailable
   */
  public String extractText(byte[] fileBytes, String filename) {
    try {
      String effectiveName = (filename != null && !filename.isBlank()) ? filename : "resume.pdf";

      ByteArrayResource resource = new ByteArrayResource(fileBytes) {
        @Override
        public String getFilename() {
          return effectiveName;
        }
      };

      MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
      body.add("file", resource);

      HttpHeaders headers = new HttpHeaders();
      headers.setContentType(MediaType.MULTIPART_FORM_DATA);

      RestTemplate restTemplate = new RestTemplate();
      ExtractTextResponse response = restTemplate.postForObject(
          properties.aiService().baseUrl() + "/api/v1/extract-text",
          new HttpEntity<>(body, headers),
          ExtractTextResponse.class);

      return (response != null && response.text() != null) ? response.text() : "";

    } catch (RestClientException ex) {
      log.warn("AI text extraction unavailable ({}), proceeding with empty text", ex.getMessage());
      return "";
    }
  }
}

