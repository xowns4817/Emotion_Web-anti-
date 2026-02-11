package com.emotion.repository;

import com.emotion.entity.ContentRecommendation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ContentRecommendationRepository extends JpaRepository<ContentRecommendation, Long> {
    List<ContentRecommendation> findByEmotionRecordId(Long emotionRecordId);
    List<ContentRecommendation> findByEmotionRecordSurveyResponseSessionId(String sessionId);
}
