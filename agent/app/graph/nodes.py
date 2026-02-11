import logging

from app.graph.state import AgentState
from app.agents.emotion_analyzer import analyze_emotion
from app.agents.content_searcher import search_contents
from app.tools.spring_callback import send_emotion_callback, send_content_callback

logger = logging.getLogger(__name__)


async def emotion_analyzer_node(state: AgentState) -> dict:
    """LangGraph 노드: 감정 분석"""
    logger.info(f"[Node] 감정 분석 시작 — sessionId: {state['session_id']}")

    try:
        emotion_result = await analyze_emotion(state["survey_answers"])

        # Spring Boot에 감정 분석 결과 콜백
        await send_emotion_callback(state["session_id"], emotion_result)

        return {
            "emotion_result": emotion_result,
            "current_step": "emotion_analyzed",
        }
    except Exception as e:
        logger.error(f"[Node] 감정 분석 실패: {e}")
        return {
            "error": str(e),
            "current_step": "emotion_failed",
        }


async def content_searcher_node(state: AgentState) -> dict:
    """LangGraph 노드: 콘텐츠 검색"""
    logger.info(f"[Node] 콘텐츠 검색 시작 — sessionId: {state['session_id']}")

    if state.get("error"):
        logger.warning(f"[Node] 이전 단계 에러로 콘텐츠 검색 스킵: {state['error']}")
        return {"current_step": "content_skipped"}

    try:
        emotion_result = state["emotion_result"]
        content_results = await search_contents(emotion_result)

        # Spring Boot에 콘텐츠 추천 결과 콜백
        await send_content_callback(state["session_id"], content_results)

        return {
            "content_results": content_results,
            "current_step": "content_searched",
        }
    except Exception as e:
        logger.error(f"[Node] 콘텐츠 검색 실패: {e}")
        return {
            "error": str(e),
            "current_step": "content_failed",
        }
