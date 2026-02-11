package com.emotion.service;

import com.emotion.dto.SurveyRequestDto;
import com.emotion.entity.SurveyResponse;
import com.emotion.repository.SurveyResponseRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class SurveyService {

    private final SurveyResponseRepository surveyResponseRepository;

    @Transactional
    public SurveyResponse submitSurvey(SurveyRequestDto request) {
        String sessionId = UUID.randomUUID().toString();

        SurveyResponse surveyResponse = SurveyResponse.builder()
                .sessionId(sessionId)
                .answers(request.getAnswers())
                .status(SurveyResponse.SurveyStatus.PENDING)
                .build();

        SurveyResponse saved = surveyResponseRepository.save(surveyResponse);
        log.info("설문 저장 완료 — sessionId: {}, id: {}", sessionId, saved.getId());
        return saved;
    }

    @Transactional(readOnly = true)
    public SurveyResponse findBySessionId(String sessionId) {
        return surveyResponseRepository.findBySessionId(sessionId)
                .orElseThrow(() -> new RuntimeException("설문을 찾을 수 없습니다: " + sessionId));
    }

    @Transactional
    public void updateStatus(String sessionId, SurveyResponse.SurveyStatus status) {
        SurveyResponse survey = findBySessionId(sessionId);
        survey.setStatus(status);
        surveyResponseRepository.save(survey);
        log.info("설문 상태 업데이트 — sessionId: {}, status: {}", sessionId, status);
    }
}
