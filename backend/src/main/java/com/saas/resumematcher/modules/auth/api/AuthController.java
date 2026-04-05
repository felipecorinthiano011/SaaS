package com.saas.resumematcher.modules.auth.api;

import com.saas.resumematcher.modules.auth.application.AuthDtos;
import com.saas.resumematcher.modules.auth.application.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@CrossOrigin(origins = {"http://localhost:4200", "http://localhost:3000", "http://127.0.0.1:4200"},
             allowedHeaders = "*",
             methods = {org.springframework.web.bind.annotation.RequestMethod.GET,
                       org.springframework.web.bind.annotation.RequestMethod.POST,
                       org.springframework.web.bind.annotation.RequestMethod.OPTIONS,
                       org.springframework.web.bind.annotation.RequestMethod.PUT,
                       org.springframework.web.bind.annotation.RequestMethod.DELETE})
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

