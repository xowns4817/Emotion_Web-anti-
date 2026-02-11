package com.emotion.dto;

import lombok.*;

import java.util.Map;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EmotionResultDto {
    private String primaryEmotion;
    private Double emotionScore;
    private Map<String, Object> emotionDetail;
    private String recommendedMood;
}
