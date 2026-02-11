package com.emotion.service;

import com.emotion.dto.AgentCallbackDto;
import com.emotion.entity.EmotionRecord;
import com.emotion.entity.SurveyResponse;
import com.emotion.repository.EmotionRecordRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class EmotionService {

    private final EmotionRecordRepository emotionRecordRepository;
    private final SurveyService surveyService;

    @Transactional
    public EmotionRecord saveEmotionResult(AgentCallbackDto.EmotionCallback callback) {
        SurveyResponse survey = surveyService.findBySessionId(callback.getSessionId());

        EmotionRecord record = EmotionRecord.builder()
                .surveyResponse(survey)
                .primaryEmotion(callback.getPrimaryEmotion())
                .emotionScore(callback.getEmotionScore())
                .emotionDetail(callback.getEmotionDetail())
                .recommendedMood(callback.getRecommendedMood())
                .build();

        EmotionRecord saved = emotionRecordRepository.save(record);

        // 설문 상태를 ANALYZING으로 업데이트
        surveyService.updateStatus(callback.getSessionId(), SurveyResponse.SurveyStatus.ANALYZING);

        log.info("감정 분석 저장 — sessionId: {}, emotion: {}, score: {}",
                callback.getSessionId(), callback.getPrimaryEmotion(), callback.getEmotionScore());
        return saved;
    }

    @Transactional(readOnly = true)
    public EmotionRecord findBySessionId(String sessionId) {
        return emotionRecordRepository.findBySurveyResponseSessionId(sessionId)
                .orElse(null);
    }
}
