package com.saas.resumematcher.modules.auth.api;

import com.saas.resumematcher.modules.auth.application.AuthDtos;
import com.saas.resumematcher.modules.auth.application.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

  private final AuthService authService;

  @PostMapping("/register")
  public ResponseEntity<AuthDtos.AuthResponse> register(
      @Valid @RequestBody AuthDtos.AuthRequest request) {
    return ResponseEntity.ok(authService.register(request));
  }

  @PostMapping("/login")
  public ResponseEntity<AuthDtos.AuthResponse> login(@Valid @RequestBody AuthDtos.AuthRequest request) {
    return ResponseEntity.ok(authService.login(request));
  }
}

