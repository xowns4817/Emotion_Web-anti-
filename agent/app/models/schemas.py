from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class AnalyzeRequest(BaseModel):
    """Spring Boot → FastAPI 분석 요청"""
    session_id: str
    survey_id: int
    answers: Dict[str, Any]


class EmotionCallbackPayload(BaseModel):
    """감정 분석 결과 콜백 (FastAPI → Spring Boot)"""
    sessionId: str
    primaryEmotion: str
    emotionScore: float
    emotionDetail: Dict[str, Any]
    recommendedMood: str


class ContentItem(BaseModel):
    """개별 콘텐츠 항목"""
    contentType: str  # QUOTE, VIDEO, IMAGE
    title: str
    contentBody: str
    source: str
    thumbnailUrl: Optional[str] = None
    relevanceScore: float


class ContentCallbackPayload(BaseModel):
    """콘텐츠 추천 결과 콜백 (FastAPI → Spring Boot)"""
    sessionId: str
    contents: List[ContentItem]


class AnalyzeResponse(BaseModel):
    """FastAPI → Spring Boot 분석 완료 응답"""
    status: str
    session_id: str
    message: str
