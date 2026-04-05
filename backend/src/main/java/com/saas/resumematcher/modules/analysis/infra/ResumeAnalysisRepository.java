package com.saas.resumematcher.modules.analysis.infra;

import com.saas.resumematcher.modules.analysis.domain.ResumeAnalysisEntity;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResumeAnalysisRepository extends JpaRepository<ResumeAnalysisEntity, Long> {
  List<ResumeAnalysisEntity> findAllByUserEmailOrderByCreatedAtDesc(String userEmail);
}

