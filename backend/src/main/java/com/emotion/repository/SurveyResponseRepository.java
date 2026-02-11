package com.emotion.repository;

import com.emotion.entity.SurveyResponse;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SurveyResponseRepository extends JpaRepository<SurveyResponse, Long> {
    Optional<SurveyResponse> findBySessionId(String sessionId);
}
