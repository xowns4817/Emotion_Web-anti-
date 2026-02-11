package com.emotion.dto;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SurveySubmitResponseDto {
    private String sessionId;
    private String status;
}
