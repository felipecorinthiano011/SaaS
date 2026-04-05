package com.saas.resumematcher.modules.resume.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Table;
import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "resumes")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ResumeEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String userEmail;

  @Column(nullable = false)
  private String fileName;

  @Lob
  @Column(nullable = false)
  private String extractedText;

  @Lob
  @Column(nullable = false)
  private byte[] fileContent;

  @Column(nullable = false)
  private String mimeType;

  @Column(nullable = false)
  private Instant uploadedAt;

  @Column(nullable = false)
  private Instant createdAt;
}

