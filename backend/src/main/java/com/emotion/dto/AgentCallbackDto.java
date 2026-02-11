package com.emotion.dto;

import lombok.*;

import java.util.List;
import java.util.Map;

/**
 * Agent 콜백 DTO — FastAPI Agent가 Spring Boot에 결과를 전송할 때 사용
 */
public class AgentCallbackDto {

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class EmotionCallback {
        private String sessionId;
        private String primaryEmotion;
        private Double emotionScore;
        private Map<String, Object> emotionDetail;
        private String recommendedMood;
    }

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class ContentCallback {
        private String sessionId;
        private List<ContentItem> contents;
    }

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class ContentItem {
        private String contentType;
        private String title;
        private String contentBody;
        private String source;
        private String thumbnailUrl;
        private Double relevanceScore;
    }
}
