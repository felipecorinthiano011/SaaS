package com.saas.resumematcher.modules.auth.infra;

import com.saas.resumematcher.modules.auth.domain.UserEntity;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<UserEntity, Long> {
  Optional<UserEntity> findByEmail(String email);
  boolean existsByEmail(String email);
}

