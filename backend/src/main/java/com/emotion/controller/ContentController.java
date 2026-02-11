package com.emotion.controller;

import com.emotion.dto.*;
import com.emotion.entity.ContentRecommendation;
import com.emotion.entity.EmotionRecord;
import com.emotion.entity.SurveyResponse;
import com.emotion.service.ContentService;
import com.emotion.service.EmotionService;
import com.emotion.service.SurveyService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class ContentController {

    private final SurveyService surveyService;
    private final EmotionService emotionService;
    private final ContentService contentService;

    /**
     * 분석 진행 상태 조회 (프론트엔드 폴링)
     */
    @GetMapping("/status/{sessionId}")
    public ResponseEntity<Map<String, String>> getStatus(@PathVariable String sessionId) {
        SurveyResponse survey = surveyService.findBySessionId(sessionId);
        return ResponseEntity.ok(Map.of(
                "sessionId", sessionId,
                "status", survey.getStatus().name()
        ));
    }

    /**
     * 추천 결과 조회
     */
    @GetMapping("/recommendations/{sessionId}")
    public ResponseEntity<RecommendationResultDto> getRecommendations(@PathVariable String sessionId) {
        SurveyResponse survey = surveyService.findBySessionId(sessionId);
        EmotionRecord emotion = emotionService.findBySessionId(sessionId);
        List<ContentRecommendation> contents = contentService.findBySessionId(sessionId);

        EmotionResultDto emotionDto = null;
        if (emotion != null) {
            emotionDto = EmotionResultDto.builder()
                    .primaryEmotion(emotion.getPrimaryEmotion())
                    .emotionScore(emotion.getEmotionScore())
                    .emotionDetail(emotion.getEmotionDetail())
                    .recommendedMood(emotion.getRecommendedMood())
                    .build();
        }

        List<ContentRecommendationDto> contentDtos = contents.stream()
                .map(c -> ContentRecommendationDto.builder()
                        .contentType(c.getContentType().name())
                        .title(c.getTitle())
                        .contentBody(c.getContentBody())
                        .source(c.getSource())
                        .thumbnailUrl(c.getThumbnailUrl())
                        .relevanceScore(c.getRelevanceScore())
                        .build())
                .toList();

        return ResponseEntity.ok(RecommendationResultDto.builder()
                .sessionId(sessionId)
                .status(survey.getStatus().name())
                .emotion(emotionDto)
                .contents(contentDtos)
                .build());
    }
}
