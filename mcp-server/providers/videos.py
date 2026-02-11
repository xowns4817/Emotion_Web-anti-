"""감정 기반 YouTube 영상 검색 프로바이더 — youtubesearchpython 사용"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# 감정별 YouTube 검색 키워드 매핑
EMOTION_SEARCH_KEYWORDS: Dict[str, List[str]] = {
    "기쁨": ["기분 좋은 음악 플레이리스트", "행복한 브이로그", "힐링 영상 웃긴"],
    "슬픔": ["위로 음악 플레이리스트", "감성 피아노 음악", "마음 위로 영상"],
    "불안": ["명상 가이드 불안 해소", "ASMR 자연 소리", "마음 안정 음악"],
    "분노": ["분노 조절 명상", "차분해지는 자연 다큐", "릴렉스 요가"],
    "평온": ["평화로운 자연 영상", "잔잔한 재즈 음악", "힐링 타임랩스"],
    "피로": ["숙면 백색 소음", "스트레칭 루틴", "릴렉싱 음악 수면"],
    "외로움": ["따뜻한 이야기 에세이", "공감 영상 위로", "힐링 다큐멘터리"],
}

EMOTION_MAP = {
    "joy": "기쁨", "sadness": "슬픔", "anxiety": "불안",
    "anger": "분노", "calm": "평온", "fatigue": "피로", "loneliness": "외로움",
    "기쁨": "기쁨", "슬픔": "슬픔", "불안": "불안",
    "분노": "분노", "평온": "평온", "피로": "피로", "외로움": "외로움",
}


def search_videos(emotion: str, count: int = 2) -> list:
    """YouTube에서 감정 기반 영상 검색 (youtubesearchpython 사용)"""
    import random

    emotion_key = EMOTION_MAP.get(emotion, "평온")
    keywords = EMOTION_SEARCH_KEYWORDS.get(emotion_key, EMOTION_SEARCH_KEYWORDS["평온"])
    search_query = random.choice(keywords)

    try:
        from youtubesearchpython import VideosSearch

        search = VideosSearch(search_query, limit=count * 2)
        raw_results = search.result().get("result", [])

        results = []
        for video in raw_results[:count]:
            thumbnail_url = None
            thumbnails = video.get("thumbnails", [])
            if thumbnails:
                thumbnail_url = thumbnails[0].get("url", "")

            results.append({
                "content_type": "VIDEO",
                "title": video.get("title", ""),
                "content_body": video.get("link", ""),
                "source": f"YouTube ({video.get('channel', {}).get('name', '알 수 없음')})",
                "thumbnail_url": thumbnail_url,
                "relevance_score": round(random.uniform(0.70, 0.90), 2),
            })

        logger.info(f"YouTube 검색 완료 — query: '{search_query}', results: {len(results)}")
        return results

    except Exception as e:
        logger.error(f"YouTube 검색 실패: {e}")
        # 폴백: 기본 추천 영상
        return _fallback_videos(emotion_key, count)


def _fallback_videos(emotion_key: str, count: int) -> list:
    """YouTube 검색 실패 시 폴백 데이터"""
    import random

    fallback = {
        "기쁨": [
            {"title": "기분 좋아지는 음악 모음", "url": "https://www.youtube.com/results?search_query=기분좋은+음악"},
            {"title": "행복 에너지 충전 영상", "url": "https://www.youtube.com/results?search_query=행복한+영상"},
        ],
        "슬픔": [
            {"title": "마음 위로하는 피아노 음악", "url": "https://www.youtube.com/results?search_query=위로+피아노+음악"},
            {"title": "감성 힐링 영상", "url": "https://www.youtube.com/results?search_query=감성+힐링"},
        ],
        "불안": [
            {"title": "불안 해소 명상 가이드", "url": "https://www.youtube.com/results?search_query=불안해소+명상"},
            {"title": "자연 소리 ASMR", "url": "https://www.youtube.com/results?search_query=자연소리+ASMR"},
        ],
        "분노": [
            {"title": "분노 조절 명상", "url": "https://www.youtube.com/results?search_query=분노조절+명상"},
            {"title": "차분해지는 자연 영상", "url": "https://www.youtube.com/results?search_query=차분한+자연+다큐"},
        ],
        "평온": [
            {"title": "평화로운 일몰 타임랩스", "url": "https://www.youtube.com/results?search_query=일몰+타임랩스"},
            {"title": "잔잔한 재즈 모음", "url": "https://www.youtube.com/results?search_query=잔잔한+재즈"},
        ],
        "피로": [
            {"title": "숙면 백색 소음", "url": "https://www.youtube.com/results?search_query=백색소음+수면"},
            {"title": "스트레칭 루틴", "url": "https://www.youtube.com/results?search_query=스트레칭+루틴"},
        ],
        "외로움": [
            {"title": "따뜻한 에세이 읽어드립니다", "url": "https://www.youtube.com/results?search_query=위로+에세이"},
            {"title": "공감 힐링 영상", "url": "https://www.youtube.com/results?search_query=공감+힐링+영상"},
        ],
    }

    videos = fallback.get(emotion_key, fallback["평온"])
    results = []
    for v in videos[:count]:
        results.append({
            "content_type": "VIDEO",
            "title": v["title"],
            "content_body": v["url"],
            "source": "YouTube (검색 링크)",
            "thumbnail_url": None,
            "relevance_score": round(random.uniform(0.60, 0.80), 2),
        })
    return results
