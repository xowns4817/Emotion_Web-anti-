package com.emotion.dto;

import lombok.*;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RecommendationResultDto {
    private String sessionId;
    private String status;
    private EmotionResultDto emotion;
    private List<ContentRecommendationDto> contents;
}
