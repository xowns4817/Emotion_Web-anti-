import logging

from app.tools.mcp_client import search_quotes, search_videos, search_images

logger = logging.getLogger(__name__)

# 감정 이름 매핑 (영문 → 한글)
EMOTION_MAP = {
    "joy": "기쁨",
    "sadness": "슬픔",
    "anxiety": "불안",
    "anger": "분노",
    "calm": "평온",
    "fatigue": "피로",
    "loneliness": "외로움",
    "기쁨": "기쁨",
    "슬픔": "슬픔",
    "불안": "불안",
    "분노": "분노",
    "평온": "평온",
    "피로": "피로",
    "외로움": "외로움",
}


async def search_contents(emotion_result: dict) -> list:
    """감정 분석 결과를 기반으로 콘텐츠 검색"""

    primary_emotion = emotion_result.get("primary_emotion", "평온")
    emotion_key = EMOTION_MAP.get(primary_emotion, "평온")

    logger.info(f"콘텐츠 검색 시작 — emotion: {emotion_key}")

    # 글귀, 영상, 이미지 병렬 검색
    quotes = await search_quotes(emotion_key, count=3)
    videos = await search_videos(emotion_key, count=2)
    images = await search_images(emotion_key, count=2)

    all_contents = quotes + videos + images

    # 기본 relevance_score 부여
    for i, content in enumerate(all_contents):
        if "relevance_score" not in content:
            content["relevance_score"] = round(0.9 - (i * 0.05), 2)

    logger.info(f"콘텐츠 검색 완료 — total: {len(all_contents)}")
    return all_contents
