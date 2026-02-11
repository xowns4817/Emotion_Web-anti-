"""MCP 콘텐츠 서버 — 감정 기반 콘텐츠(글귀/영상/이미지) 검색 API"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from providers.quotes import search_quotes
from providers.videos import search_videos
from providers.images import search_images

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Emotion MCP Content Server",
    description="감정 기반 콘텐츠 검색 서버 (글귀, 영상, 이미지)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    emotion: str
    count: Optional[int] = None


class SearchAllRequest(BaseModel):
    emotion: str
    quote_count: int = 3
    video_count: int = 2
    image_count: int = 2


@app.get("/health")
async def health():
    return {"status": "ok", "service": "mcp-content-server"}


@app.post("/search/quotes")
async def api_search_quotes(request: SearchRequest):
    """감정 기반 글귀 검색"""
    count = request.count or 3
    results = search_quotes(request.emotion, count)
    logger.info(f"글귀 검색 — emotion: {request.emotion}, count: {len(results)}")
    return {"results": results}


@app.post("/search/videos")
async def api_search_videos(request: SearchRequest):
    """감정 기반 YouTube 영상 검색"""
    count = request.count or 2
    results = search_videos(request.emotion, count)
    logger.info(f"영상 검색 — emotion: {request.emotion}, count: {len(results)}")
    return {"results": results}


@app.post("/search/images")
async def api_search_images(request: SearchRequest):
    """감정 기반 이미지 검색"""
    count = request.count or 2
    results = search_images(request.emotion, count)
    logger.info(f"이미지 검색 — emotion: {request.emotion}, count: {len(results)}")
    return {"results": results}


@app.post("/search/all")
async def api_search_all(request: SearchAllRequest):
    """감정 기반 전체 콘텐츠 통합 검색"""
    quotes = search_quotes(request.emotion, request.quote_count)
    videos = search_videos(request.emotion, request.video_count)
    images = search_images(request.emotion, request.image_count)

    all_results = quotes + videos + images
    logger.info(f"통합 검색 — emotion: {request.emotion}, total: {len(all_results)}")
    return {"results": all_results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
