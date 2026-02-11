package com.emotion.controller;

import com.emotion.dto.AgentCallbackDto;
import com.emotion.service.ContentService;
import com.emotion.service.EmotionService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/callback")
@RequiredArgsConstructor
public class AgentCallbackController {

    private final EmotionService emotionService;
    private final ContentService contentService;

    /**
     * 감정 분석 결과 콜백 (FastAPI Agent → Spring Boot)
     */
    @PostMapping("/emotion")
    public ResponseEntity<Map<String, String>> emotionCallback(@RequestBody AgentCallbackDto.EmotionCallback callback) {
        log.info("감정 분석 콜백 수신 — sessionId: {}, emotion: {}", callback.getSessionId(), callback.getPrimaryEmotion());
        emotionService.saveEmotionResult(callback);
        return ResponseEntity.ok(Map.of("status", "saved"));
    }

    /**
     * 콘텐츠 추천 결과 콜백 (FastAPI Agent → Spring Boot)
     */
    @PostMapping("/content")
    public ResponseEntity<Map<String, String>> contentCallback(@RequestBody AgentCallbackDto.ContentCallback callback) {
        log.info("콘텐츠 추천 콜백 수신 — sessionId: {}, count: {}", callback.getSessionId(), callback.getContents().size());
        contentService.saveContentResults(callback);
        return ResponseEntity.ok(Map.of("status", "saved"));
    }
}
