package com.emotion.controller;

import com.emotion.dto.*;
import com.emotion.entity.SurveyResponse;
import com.emotion.service.AgentClient;
import com.emotion.service.SurveyService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/survey")
@RequiredArgsConstructor
public class SurveyController {

    private final SurveyService surveyService;
    private final AgentClient agentClient;

    /**
     * 설문 문항 목록 조회
     */
    @GetMapping("/questions")
    public ResponseEntity<List<Map<String, Object>>> getQuestions() {
        List<Map<String, Object>> questions = List.of(
                Map.of(
                        "id", 1,
                        "question", "지금 기분을 이모지로 표현하면?",
                        "type", "EMOJI_SELECT",
                        "options", List.of(
                                Map.of("emoji", "😊", "label", "기쁨", "value", "JOY"),
                                Map.of("emoji", "😢", "label", "슬픔", "value", "SADNESS"),
                                Map.of("emoji", "😡", "label", "분노", "value", "ANGER"),
                                Map.of("emoji", "😰", "label", "불안", "value", "ANXIETY"),
                                Map.of("emoji", "😌", "label", "평온", "value", "CALM"),
                                Map.of("emoji", "😩", "label", "피로", "value", "FATIGUE"),
                                Map.of("emoji", "🥺", "label", "외로움", "value", "LONELINESS")
                        )
                ),
                Map.of(
                        "id", 2,
                        "question", "오늘 에너지 레벨은?",
                        "type", "SLIDER",
                        "min", 1,
                        "max", 10
                ),
                Map.of(
                        "id", 3,
                        "question", "가장 크게 느끼는 감정은?",
                        "type", "SINGLE_SELECT",
                        "options", List.of("기쁨", "슬픔", "분노", "불안", "평온", "피로", "외로움")
                ),
                Map.of(
                        "id", 4,
                        "question", "그 감정의 강도는?",
                        "type", "SLIDER",
                        "min", 1,
                        "max", 10
                ),
                Map.of(
                        "id", 5,
                        "question", "최근 스트레스 원인은?",
                        "type", "MULTI_SELECT",
                        "options", List.of("일/업무", "인간관계", "건강", "재정", "학업", "기타")
                ),
                Map.of(
                        "id", 6,
                        "question", "원하는 위안의 형태는?",
                        "type", "SINGLE_SELECT",
                        "options", List.of("따뜻한 말", "활력/동기부여", "평온/힐링", "재미/유머", "위로/공감")
                ),
                Map.of(
                        "id", 7,
                        "question", "추가로 표현하고 싶은 감정이 있나요?",
                        "type", "FREE_TEXT",
                        "required", false
                )
        );
        return ResponseEntity.ok(questions);
    }

    /**
     * 설문 제출 → DB 저장 → Agent 분석 요청
     */
    @PostMapping("/submit")
    public ResponseEntity<SurveySubmitResponseDto> submitSurvey(@Valid @RequestBody SurveyRequestDto request) {
        // 1. 설문 저장
        SurveyResponse saved = surveyService.submitSurvey(request);

        // 2. Agent에 비동기 분석 요청
        agentClient.requestAnalysis(saved.getSessionId(), saved.getId(), saved.getAnswers());

        // 3. sessionId 반환
        return ResponseEntity.ok(SurveySubmitResponseDto.builder()
                .sessionId(saved.getSessionId())
                .status(saved.getStatus().name())
                .build());
    }
}
