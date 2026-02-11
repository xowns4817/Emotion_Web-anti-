import { useState, useEffect, useCallback } from 'react';
import type { SurveyQuestion, SurveyAnswers } from '../../types';
import { fetchQuestions, submitSurvey, fetchStatus, fetchRecommendations } from '../../api/emotionApi';
import type { RecommendationResult } from '../../types';
import './SurveyPage.css';

interface SurveyPageProps {
    onComplete: (result: RecommendationResult) => void;
}

export default function SurveyPage({ onComplete }: SurveyPageProps) {
    const [questions, setQuestions] = useState<SurveyQuestion[]>([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [answers, setAnswers] = useState<SurveyAnswers>({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [analyzeStatus, setAnalyzeStatus] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        fetchQuestions()
            .then(setQuestions)
            .catch(() => setError('설문을 불러오는데 실패했습니다.'));
    }, []);

    const handleAnswer = (questionId: number, value: string | number | string[]) => {
        setAnswers((prev) => ({ ...prev, [String(questionId)]: value }));
    };

    const handleNext = () => {
        if (currentStep < questions.length - 1) {
            setCurrentStep((prev) => prev + 1);
        }
    };

    const handlePrev = () => {
        if (currentStep > 0) {
            setCurrentStep((prev) => prev - 1);
        }
    };

    const pollForResults = useCallback(async (sessionId: string) => {
        setAnalyzeStatus('감정을 분석하고 있어요...');

        const maxAttempts = 60;
        for (let i = 0; i < maxAttempts; i++) {
            await new Promise((r) => setTimeout(r, 2000));

            try {
                const status = await fetchStatus(sessionId);

                if (status.status === 'ANALYZING') {
                    setAnalyzeStatus('맞춤 콘텐츠를 찾고 있어요...');
                }

                if (status.status === 'COMPLETED') {
                    const result = await fetchRecommendations(sessionId);
                    onComplete(result);
                    return;
                }

                if (status.status === 'FAILED') {
                    setError('분석에 실패했습니다. 다시 시도해 주세요.');
                    setIsAnalyzing(false);
                    return;
                }
            } catch {
                // 폴링 실패 시 계속 시도
            }
        }

        setError('분석 시간이 초과되었습니다. 다시 시도해 주세요.');
        setIsAnalyzing(false);
    }, [onComplete]);

    const handleSubmit = async () => {
        setIsSubmitting(true);
        setError('');

        try {
            const response = await submitSurvey(answers);
            setIsSubmitting(false);
            setIsAnalyzing(true);
            pollForResults(response.sessionId);
        } catch {
            setError('설문 제출에 실패했습니다.');
            setIsSubmitting(false);
        }
    };

    if (error && !isAnalyzing) {
        return (
            <div className="survey-page">
                <div className="error-card">
                    <p>{error}</p>
                    <button onClick={() => window.location.reload()}>다시 시도</button>
                </div>
            </div>
        );
    }

    if (isAnalyzing) {
        return (
            <div className="survey-page">
                <div className="analyzing-card">
                    <div className="analyzing-spinner"></div>
                    <p className="analyzing-text">{analyzeStatus}</p>
                    <div className="analyzing-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        );
    }

    if (questions.length === 0) {
        return (
            <div className="survey-page">
                <div className="loading-card">
                    <div className="analyzing-spinner"></div>
                    <p>설문을 불러오는 중...</p>
                </div>
            </div>
        );
    }

    const question = questions[currentStep];
    const progress = ((currentStep + 1) / questions.length) * 100;
    const isLastStep = currentStep === questions.length - 1;
    const currentAnswer = answers[String(question.id)];
    const canProceed = question.type === 'FREE_TEXT'
        ? true
        : currentAnswer !== undefined && currentAnswer !== '';

    return (
        <div className="survey-page">
            <div className="survey-card">
                {/* Progress Bar */}
                <div className="progress-bar-container">
                    <div className="progress-bar" style={{ width: `${progress}%` }}></div>
                </div>
                <p className="progress-text">{currentStep + 1} / {questions.length}</p>

                {/* Question */}
                <h2 className="question-text">{question.question}</h2>

                {/* Answer Input */}
                <div className="answer-section">
                    {question.type === 'EMOJI_SELECT' && (
                        <div className="emoji-grid">
                            {(question.options as Array<{ emoji: string; label: string; value: string }>)?.map((opt) => (
                                <button
                                    key={opt.value}
                                    className={`emoji-btn ${currentAnswer === opt.value ? 'selected' : ''}`}
                                    onClick={() => handleAnswer(question.id, opt.value)}
                                >
                                    <span className="emoji">{opt.emoji}</span>
                                    <span className="emoji-label">{opt.label}</span>
                                </button>
                            ))}
                        </div>
                    )}

                    {question.type === 'SLIDER' && (
                        <div className="slider-container">
                            <input
                                type="range"
                                min={question.min || 1}
                                max={question.max || 10}
                                value={(currentAnswer as number) || question.min || 1}
                                onChange={(e) => handleAnswer(question.id, Number(e.target.value))}
                                className="slider"
                            />
                            <div className="slider-labels">
                                <span>{question.min || 1}</span>
                                <span className="slider-value">{(currentAnswer as number) || question.min || 1}</span>
                                <span>{question.max || 10}</span>
                            </div>
                        </div>
                    )}

                    {question.type === 'SINGLE_SELECT' && (
                        <div className="select-grid">
                            {(question.options as string[])?.map((opt) => (
                                <button
                                    key={opt}
                                    className={`select-btn ${currentAnswer === opt ? 'selected' : ''}`}
                                    onClick={() => handleAnswer(question.id, opt)}
                                >
                                    {opt}
                                </button>
                            ))}
                        </div>
                    )}

                    {question.type === 'MULTI_SELECT' && (
                        <div className="select-grid">
                            {(question.options as string[])?.map((opt) => {
                                const selectedArr = (currentAnswer as string[]) || [];
                                const isSelected = selectedArr.includes(opt);
                                return (
                                    <button
                                        key={opt}
                                        className={`select-btn ${isSelected ? 'selected' : ''}`}
                                        onClick={() => {
                                            const newArr = isSelected
                                                ? selectedArr.filter((v) => v !== opt)
                                                : [...selectedArr, opt];
                                            handleAnswer(question.id, newArr);
                                        }}
                                    >
                                        {opt}
                                    </button>
                                );
                            })}
                        </div>
                    )}

                    {question.type === 'FREE_TEXT' && (
                        <textarea
                            className="free-text-input"
                            placeholder="자유롭게 적어주세요 (선택)"
                            value={(currentAnswer as string) || ''}
                            onChange={(e) => handleAnswer(question.id, e.target.value)}
                            rows={4}
                        />
                    )}
                </div>

                {/* Navigation */}
                <div className="nav-buttons">
                    <button
                        className="nav-btn prev"
                        onClick={handlePrev}
                        disabled={currentStep === 0}
                    >
                        ← 이전
                    </button>

                    {isLastStep ? (
                        <button
                            className="nav-btn submit"
                            onClick={handleSubmit}
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? '제출 중...' : '제출하기 ✨'}
                        </button>
                    ) : (
                        <button
                            className="nav-btn next"
                            onClick={handleNext}
                            disabled={!canProceed}
                        >
                            다음 →
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
