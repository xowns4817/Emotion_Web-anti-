"""MCP 클라이언트 — Public MCP Server(Brave Search)를 호출하여 콘텐츠 검색

Agent가 MCP 클라이언트로서 외부 MCP 서버의 Tool을 호출하는 구조:
  Agent (MCP Client) → stdio → npx @anthropic-ai/server-brave-search → Brave API

Brave Search API Key가 없는 경우 로컬 폴백 데이터를 사용합니다.
"""

import asyncio
import json
import logging
import os
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.config import MCP_SERVER_URL

logger = logging.getLogger(__name__)

# 감정 → 검색 쿼리 매핑
EMOTION_SEARCH_QUERIES = {
    "기쁨": {
        "quotes": "행복 기쁨 명언 위로 한국어",
        "videos": "기분 좋은 힐링 음악 플레이리스트 site:youtube.com",
        "images": "bright happy sunshine flowers nature",
    },
    "슬픔": {
        "quotes": "슬플 때 위로 명언 한국어",
        "videos": "위로 감성 피아노 음악 site:youtube.com",
        "images": "rain window melancholy calm lake",
    },
    "불안": {
        "quotes": "불안할 때 도움 명언 마음 안정",
        "videos": "불안 해소 명상 가이드 ASMR site:youtube.com",
        "images": "calm ocean peaceful forest zen",
    },
    "분노": {
        "quotes": "화날 때 마음 다스리는 명언",
        "videos": "분노 조절 명상 차분한 자연 site:youtube.com",
        "images": "serene sea calm mountain green nature",
    },
    "평온": {
        "quotes": "평온 고요 명언 명상",
        "videos": "평화로운 자연 힐링 재즈 site:youtube.com",
        "images": "sunset golden hour peaceful lake reflection",
    },
    "피로": {
        "quotes": "지칠 때 위로 명언 쉼",
        "videos": "숙면 백색소음 릴렉싱 음악 site:youtube.com",
        "images": "cozy coffee warm blanket comfortable rest",
    },
    "외로움": {
        "quotes": "외로울 때 위로 명언 따뜻한 말",
        "videos": "따뜻한 이야기 에세이 공감 힐링 site:youtube.com",
        "images": "candlelight warm starry night togetherness",
    },
}

EMOTION_MAP = {
    "joy": "기쁨", "sadness": "슬픔", "anxiety": "불안",
    "anger": "분노", "calm": "평온", "fatigue": "피로", "loneliness": "외로움",
    "기쁨": "기쁨", "슬픔": "슬픔", "불안": "불안",
    "분노": "분노", "평온": "평온", "피로": "피로", "외로움": "외로움",
}


async def _call_brave_search(query: str, count: int = 5) -> list:
    """Brave Search MCP 서버를 stdio로 호출하여 웹 검색 수행"""

    brave_api_key = os.getenv("BRAVE_API_KEY", "")
    if not brave_api_key:
        logger.warning("BRAVE_API_KEY가 설정되지 않음 — 폴백 데이터 사용")
        return []

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-brave-search"],
        env={"BRAVE_API_KEY": brave_api_key, "PATH": os.environ.get("PATH", "")},
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "brave_web_search",
                    arguments={"query": query, "count": count},
                )

                if result.content:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    return json.loads(text) if text.startswith('[') or text.startswith('{') else [{"raw": text}]

                return []

    except Exception as e:
        logger.error(f"Brave Search MCP 호출 실패: {e}")
        return []


# ──────────────────────────────────────────────
#  폴백 로컬 데이터 (Brave API Key 없을 때)
# ──────────────────────────────────────────────
from app.tools._fallback_data import FALLBACK_QUOTES, FALLBACK_VIDEOS, FALLBACK_IMAGES
import random


async def search_quotes(emotion: str, count: int = 3) -> list:
    """감정 기반 글귀 검색 — MCP(Brave Search) 또는 폴백"""
    emotion_key = EMOTION_MAP.get(emotion, "평온")

    # 1) Brave Search MCP 시도
    query = EMOTION_SEARCH_QUERIES.get(emotion_key, {}).get("quotes", f"{emotion_key} 명언 위로")
    results = await _call_brave_search(query, count=count + 2)

    if results and isinstance(results, list) and not results[0].get("raw"):
        parsed = []
        for r in results[:count]:
            parsed.append({
                "content_type": "QUOTE",
                "title": r.get("title", "명언"),
                "content_body": r.get("description", r.get("snippet", "")),
                "source": r.get("url", "웹 검색"),
                "thumbnail_url": None,
                "relevance_score": round(random.uniform(0.75, 0.95), 2),
            })
        logger.info(f"Brave Search 글귀 검색 완료 — emotion: {emotion_key}, count: {len(parsed)}")
        return parsed

    # 2) 폴백: 로컬 데이터
    quotes = FALLBACK_QUOTES.get(emotion_key, FALLBACK_QUOTES.get("평온", []))
    selected = random.sample(quotes, min(count, len(quotes)))
    results = []
    for q in selected:
        results.append({
            "content_type": "QUOTE",
            "title": q["title"],
            "content_body": f"{q['body']} — {q['author']}",
            "source": f"명언 데이터베이스 ({q['author']})",
            "thumbnail_url": None,
            "relevance_score": round(random.uniform(0.75, 0.95), 2),
        })
    logger.info(f"폴백 글귀 — emotion: {emotion_key}, count: {len(results)}")
    return results


async def search_videos(emotion: str, count: int = 2) -> list:
    """감정 기반 영상 검색 — MCP(Brave Search) 또는 폴백"""
    emotion_key = EMOTION_MAP.get(emotion, "평온")

    # 1) Brave Search MCP 시도
    query = EMOTION_SEARCH_QUERIES.get(emotion_key, {}).get("videos", f"{emotion_key} 힐링 영상 youtube")
    results = await _call_brave_search(query, count=count + 2)

    if results and isinstance(results, list) and not results[0].get("raw"):
        parsed = []
        for r in results[:count]:
            url = r.get("url", "")
            if "youtube.com" in url or "youtu.be" in url:
                parsed.append({
                    "content_type": "VIDEO",
                    "title": r.get("title", "영상"),
                    "content_body": url,
                    "source": "YouTube (Brave Search)",
                    "thumbnail_url": r.get("thumbnail", None),
                    "relevance_score": round(random.uniform(0.70, 0.90), 2),
                })
        if parsed:
            logger.info(f"Brave Search 영상 검색 완료 — emotion: {emotion_key}, count: {len(parsed)}")
            return parsed[:count]

    # 2) 폴백: 로컬 데이터
    videos = FALLBACK_VIDEOS.get(emotion_key, FALLBACK_VIDEOS.get("평온", []))
    selected = random.sample(videos, min(count, len(videos)))
    results = []
    for v in selected:
        results.append({
            "content_type": "VIDEO",
            "title": v["title"],
            "content_body": v["url"],
            "source": "YouTube (추천)",
            "thumbnail_url": v.get("thumbnail"),
            "relevance_score": round(random.uniform(0.70, 0.90), 2),
        })
    logger.info(f"폴백 영상 — emotion: {emotion_key}, count: {len(results)}")
    return results


async def search_images(emotion: str, count: int = 2) -> list:
    """감정 기반 이미지 검색 — MCP(Brave Search) 또는 폴백"""
    emotion_key = EMOTION_MAP.get(emotion, "평온")

    # 1) Brave Search MCP 시도
    query = EMOTION_SEARCH_QUERIES.get(emotion_key, {}).get("images", f"{emotion_key} aesthetic calm")
    results = await _call_brave_search(query, count=count + 2)

    if results and isinstance(results, list) and not results[0].get("raw"):
        parsed = []
        for r in results[:count]:
            img_url = r.get("thumbnail", r.get("url", ""))
            if img_url:
                parsed.append({
                    "content_type": "IMAGE",
                    "title": r.get("title", "이미지"),
                    "content_body": img_url,
                    "source": "웹 검색 (Brave Search)",
                    "thumbnail_url": img_url,
                    "relevance_score": round(random.uniform(0.70, 0.92), 2),
                })
        if parsed:
            logger.info(f"Brave Search 이미지 검색 완료 — emotion: {emotion_key}, count: {len(parsed)}")
            return parsed[:count]

    # 2) 폴백: 큐레이팅 Pexels 이미지
    images = FALLBACK_IMAGES.get(emotion_key, FALLBACK_IMAGES.get("평온", []))
    selected = random.sample(images, min(count, len(images)))
    results = []
    for img in selected:
        results.append({
            "content_type": "IMAGE",
            "title": img["title"],
            "content_body": img["url"],
            "source": "Pexels (무료 이미지)",
            "thumbnail_url": img["thumb"],
            "relevance_score": round(random.uniform(0.70, 0.92), 2),
        })
    logger.info(f"폴백 이미지 — emotion: {emotion_key}, count: {len(results)}")
    return results
