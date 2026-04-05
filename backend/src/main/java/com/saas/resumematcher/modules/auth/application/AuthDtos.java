package com.saas.resumematcher.modules.auth.application;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public final class AuthDtos {

  private AuthDtos() {}

  public record AuthRequest(@Email @NotBlank String email, @NotBlank String password) {}

  public record AuthResponse(String token) {}
}

