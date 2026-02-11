import httpx
import logging

from app.config import SPRING_BOOT_URL

logger = logging.getLogger(__name__)


async def send_emotion_callback(session_id: str, emotion_result: dict) -> None:
    """감정 분석 결과를 Spring Boot에 콜백 전송"""
    payload = {
        "sessionId": session_id,
        "primaryEmotion": emotion_result.get("primary_emotion", ""),
        "emotionScore": emotion_result.get("emotion_score", 0.0),
        "emotionDetail": emotion_result.get("emotion_detail", {}),
        "recommendedMood": emotion_result.get("recommended_mood", ""),
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SPRING_BOOT_URL}/api/callback/emotion",
                json=payload,
                timeout=10.0,
            )
            response.raise_for_status()
            logger.info(f"감정 콜백 전송 성공 — sessionId: {session_id}")
        except Exception as e:
            logger.error(f"감정 콜백 전송 실패 — sessionId: {session_id}, error: {e}")
            raise


async def send_content_callback(session_id: str, contents: list) -> None:
    """콘텐츠 추천 결과를 Spring Boot에 콜백 전송"""
    payload = {
        "sessionId": session_id,
        "contents": [
            {
                "contentType": c.get("content_type", ""),
                "title": c.get("title", ""),
                "contentBody": c.get("content_body", ""),
                "source": c.get("source", ""),
                "thumbnailUrl": c.get("thumbnail_url"),
                "relevanceScore": c.get("relevance_score", 0.0),
            }
            for c in contents
        ],
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SPRING_BOOT_URL}/api/callback/content",
                json=payload,
                timeout=10.0,
            )
            response.raise_for_status()
            logger.info(f"콘텐츠 콜백 전송 성공 — sessionId: {session_id}")
        except Exception as e:
            logger.error(f"콘텐츠 콜백 전송 실패 — sessionId: {session_id}, error: {e}")
            raise
