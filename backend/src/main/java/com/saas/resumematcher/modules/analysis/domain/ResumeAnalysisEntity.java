package com.saas.resumematcher.modules.analysis.domain;

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
@Table(name = "resume_analyses")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ResumeAnalysisEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String userEmail;

  @Lob
  @Column(nullable = false)
  private String jobDescription;

  @Lob
  @Column(nullable = false)
  private String resumeText;

  @Column(nullable = false)
  private Integer atsScore;

  @Lob
  @Column(nullable = false)
  private String extractedKeywords;

  @Lob
  @Column(nullable = false)
  private String optimizedResume;

  @Lob
  @Column(nullable = false)
  private String gapSummary;

  @Column(nullable = false)
  private Instant createdAt;
}

