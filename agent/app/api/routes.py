import logging
from fastapi import APIRouter, BackgroundTasks
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.graph.workflow import agent_workflow
from app.config import SPRING_BOOT_URL

logger = logging.getLogger(__name__)

router = APIRouter()


async def run_analysis(session_id: str, survey_id: int, answers: dict):
    """백그라운드에서 LangGraph 워크플로우 실행"""
    try:
        initial_state = {
            "session_id": session_id,
            "survey_id": survey_id,
            "survey_answers": answers,
            "callback_url": SPRING_BOOT_URL,
            "emotion_result": None,
            "content_results": None,
            "current_step": "started",
            "error": None,
        }

        result = await agent_workflow.ainvoke(initial_state)
        logger.info(f"워크플로우 완료 — sessionId: {session_id}, step: {result.get('current_step')}")

    except Exception as e:
        logger.error(f"워크플로우 실행 실패 — sessionId: {session_id}, error: {e}")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_emotion(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """Spring Boot에서 호출 — 설문 데이터 기반 감정 분석 + 콘텐츠 추천 시작

    분석은 백그라운드에서 비동기 실행되며, 결과는 콜백으로 Spring Boot에 전송됩니다.
    """
    logger.info(f"분석 요청 수신 — sessionId: {request.session_id}, surveyId: {request.survey_id}")

    background_tasks.add_task(
        run_analysis,
        request.session_id,
        request.survey_id,
        request.answers,
    )

    return AnalyzeResponse(
        status="processing",
        session_id=request.session_id,
        message="분석이 시작되었습니다. 결과는 콜백으로 전송됩니다.",
    )
