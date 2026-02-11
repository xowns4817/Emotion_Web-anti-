package com.emotion.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Slf4j
@Service
public class AgentClient {

    private final WebClient agentWebClient;

    public AgentClient(@Qualifier("agentWebClient") WebClient agentWebClient) {
        this.agentWebClient = agentWebClient;
    }

    /**
     * FastAPI Agent 서버에 분석 요청
     */
    public void requestAnalysis(String sessionId, Long surveyId, Map<String, Object> answers) {
        Map<String, Object> requestBody = Map.of(
                "session_id", sessionId,
                "survey_id", surveyId,
                "answers", answers
        );

        agentWebClient.post()
                .uri("/analyze")
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(Map.class)
                .doOnSuccess(response -> log.info("Agent 분석 요청 전송 완료 — sessionId: {}", sessionId))
                .doOnError(error -> log.error("Agent 분석 요청 실패 — sessionId: {}, error: {}", sessionId, error.getMessage()))
                .subscribe(); // 비동기 fire-and-forget
    }
}
