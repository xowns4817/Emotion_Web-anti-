package com.emotion.service;

import com.emotion.dto.AgentCallbackDto;
import com.emotion.entity.ContentRecommendation;
import com.emotion.entity.EmotionRecord;
import com.emotion.entity.SurveyResponse;
import com.emotion.repository.ContentRecommendationRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class ContentService {

    private final ContentRecommendationRepository contentRecommendationRepository;
    private final EmotionService emotionService;
    private final SurveyService surveyService;

    @Transactional
    public List<ContentRecommendation> saveContentResults(AgentCallbackDto.ContentCallback callback) {
        EmotionRecord emotionRecord = emotionService.findBySessionId(callback.getSessionId());
        if (emotionRecord == null) {
            throw new RuntimeException("감정 분석 결과를 찾을 수 없습니다: " + callback.getSessionId());
        }

        List<ContentRecommendation> recommendations = callback.getContents().stream()
                .map(item -> ContentRecommendation.builder()
                        .emotionRecord(emotionRecord)
                        .contentType(ContentRecommendation.ContentType.valueOf(item.getContentType()))
                        .title(item.getTitle())
                        .contentBody(item.getContentBody())
                        .source(item.getSource())
                        .thumbnailUrl(item.getThumbnailUrl())
                        .relevanceScore(item.getRelevanceScore())
                        .build())
                .toList();

        List<ContentRecommendation> saved = contentRecommendationRepository.saveAll(recommendations);

        // 설문 상태를 COMPLETED로 업데이트
        surveyService.updateStatus(callback.getSessionId(), SurveyResponse.SurveyStatus.COMPLETED);

        log.info("콘텐츠 추천 저장 — sessionId: {}, count: {}", callback.getSessionId(), saved.size());
        return saved;
    }

    @Transactional(readOnly = true)
    public List<ContentRecommendation> findBySessionId(String sessionId) {
        return contentRecommendationRepository.findByEmotionRecordSurveyResponseSessionId(sessionId);
    }
}
