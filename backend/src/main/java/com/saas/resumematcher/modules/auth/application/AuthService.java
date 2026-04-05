package com.saas.resumematcher.modules.auth.application;

import com.saas.resumematcher.common.security.JwtService;
import com.saas.resumematcher.modules.auth.domain.UserEntity;
import com.saas.resumematcher.modules.auth.infra.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

  private final UserRepository userRepository;
  private final PasswordEncoder passwordEncoder;
  private final JwtService jwtService;
  private final AuthenticationManager authenticationManager;

  public AuthDtos.AuthResponse register(AuthDtos.AuthRequest request) {
    if (userRepository.existsByEmail(request.email())) {
      throw new IllegalArgumentException("Email already registered");
    }

    UserEntity user =
        UserEntity.builder().email(request.email()).password(passwordEncoder.encode(request.password())).build();

    UserEntity savedUser = userRepository.save(user);
    return new AuthDtos.AuthResponse(jwtService.generateToken(savedUser));
  }

  public AuthDtos.AuthResponse login(AuthDtos.AuthRequest request) {
    authenticationManager.authenticate(
        new UsernamePasswordAuthenticationToken(request.email(), request.password()));

    UserEntity user =
        userRepository
            .findByEmail(request.email())
            .orElseThrow(() -> new IllegalArgumentException("Invalid credentials"));

    return new AuthDtos.AuthResponse(jwtService.generateToken(user));
  }
}

