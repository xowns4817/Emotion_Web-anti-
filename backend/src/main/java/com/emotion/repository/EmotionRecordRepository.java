package com.emotion.repository;

import com.emotion.entity.EmotionRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface EmotionRecordRepository extends JpaRepository<EmotionRecord, Long> {
    Optional<EmotionRecord> findBySurveyResponseId(Long surveyResponseId);
    Optional<EmotionRecord> findBySurveyResponseSessionId(String sessionId);
}
