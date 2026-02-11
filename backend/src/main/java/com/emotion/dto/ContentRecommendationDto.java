package com.emotion.dto;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ContentRecommendationDto {
    private String contentType;
    private String title;
    private String contentBody;
    private String source;
    private String thumbnailUrl;
    private Double relevanceScore;
}
