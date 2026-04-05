package com.saas.resumematcher.modules.resume.infra;

import com.saas.resumematcher.modules.resume.domain.ResumeEntity;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface ResumeRepository extends JpaRepository<ResumeEntity, Long> {
  List<ResumeEntity> findAllByUserEmailOrderByUploadedAtDesc(String userEmail);

  @Query(value = "SELECT * FROM resumes WHERE user_email = ?1 ORDER BY uploaded_at DESC LIMIT 1", nativeQuery = true)
  Optional<ResumeEntity> findLatestByUserEmail(String userEmail);
}

