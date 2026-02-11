package com.emotion.dto;

import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.util.Map;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SurveyRequestDto {

    @NotNull(message = "설문 답변은 필수입니다")
    private Map<String, Object> answers;
}
