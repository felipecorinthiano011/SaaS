package com.saas.resumematcher.common.security;

import com.saas.resumematcher.common.config.ApplicationProperties;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Date;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class JwtService {

  private final ApplicationProperties properties;

  public String extractUsername(String token) {
    return extractAllClaims(token).getSubject();
  }

  public String generateToken(UserDetails userDetails) {
    Instant now = Instant.now();
    Instant expiration = now.plusSeconds(properties.jwt().expirationSeconds());

    return Jwts.builder()
        .claims(Map.of())
        .subject(userDetails.getUsername())
        .issuedAt(Date.from(now))
        .expiration(Date.from(expiration))
        .signWith(getSigningKey())
        .compact();
  }

  public boolean isTokenValid(String token, UserDetails userDetails) {
    String username = extractUsername(token);
    return username.equals(userDetails.getUsername()) && !isTokenExpired(token);
  }

  private boolean isTokenExpired(String token) {
    return extractAllClaims(token).getExpiration().before(new Date());
  }

  private Claims extractAllClaims(String token) {
    return Jwts.parser().verifyWith(getSigningKey()).build().parseSignedClaims(token).getPayload();
  }

  private javax.crypto.SecretKey getSigningKey() {
    byte[] keyBytes = properties.jwt().secret().getBytes(StandardCharsets.UTF_8);
    return Keys.hmacShaKeyFor(keyBytes);
  }
}
