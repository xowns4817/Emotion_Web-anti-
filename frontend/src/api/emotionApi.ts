import type {
    SurveyQuestion,
    SurveyAnswers,
    SurveySubmitResponse,
    StatusResponse,
    RecommendationResult,
} from '../types';

const API_BASE = 'http://localhost:8080/api';

export async function fetchQuestions(): Promise<SurveyQuestion[]> {
    const res = await fetch(`${API_BASE}/survey/questions`);
    if (!res.ok) throw new Error('설문 문항을 가져올 수 없습니다');
    return res.json();
}

export async function submitSurvey(answers: SurveyAnswers): Promise<SurveySubmitResponse> {
    const res = await fetch(`${API_BASE}/survey/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers }),
    });
    if (!res.ok) throw new Error('설문 제출에 실패했습니다');
    return res.json();
}

export async function fetchStatus(sessionId: string): Promise<StatusResponse> {
    const res = await fetch(`${API_BASE}/status/${sessionId}`);
    if (!res.ok) throw new Error('상태 조회에 실패했습니다');
    return res.json();
}

export async function fetchRecommendations(sessionId: string): Promise<RecommendationResult> {
    const res = await fetch(`${API_BASE}/recommendations/${sessionId}`);
    if (!res.ok) throw new Error('추천 결과를 가져올 수 없습니다');
    return res.json();
}
