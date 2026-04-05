package com.saas.resumematcher.common.api;

import java.time.Instant;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler(IllegalArgumentException.class)
  public ResponseEntity<Map<String, Object>> handleIllegalArgument(IllegalArgumentException ex) {
    return ResponseEntity.badRequest()
        .body(Map.of("timestamp", Instant.now().toString(), "message", ex.getMessage()));
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
    return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
        .body(
            Map.of(
                "timestamp",
                Instant.now().toString(),
                "message",
                "Validation failed",
                "errors",
                ex.getBindingResult().getFieldErrors().stream()
                    .map(error -> Map.of("field", error.getField(), "message", error.getDefaultMessage()))
                    .toList()));
  }
}

