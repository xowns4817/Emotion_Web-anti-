import json
import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from app.config import LLM_API_KEY, LLM_MODEL
from app.prompts.emotion_prompt import EMOTION_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


async def analyze_emotion(survey_answers: dict) -> dict:
    """LLM(Gemini)을 사용하여 설문 답변을 분석하고 감정 결과를 반환"""

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=LLM_API_KEY,
        temperature=0.3,
    )

    prompt = EMOTION_ANALYSIS_PROMPT.format(
        survey_answers=json.dumps(survey_answers, ensure_ascii=False, indent=2)
    )

    try:
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        content = response.content

        # JSON 파싱 (마크다운 코드블록 제거)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        result = json.loads(content.strip())
        logger.info(f"감정 분석 완료 — primary: {result.get('primary_emotion')}, score: {result.get('emotion_score')}")
        return result

    except Exception as e:
        logger.error(f"감정 분석 실패: {e}")
        # 폴백: 기본 분석 결과
        return {
            "primary_emotion": "평온",
            "emotion_score": 0.5,
            "emotion_detail": {
                "joy": 0.0, "sadness": 0.0, "anxiety": 0.0,
                "anger": 0.0, "calm": 0.5, "fatigue": 0.0, "loneliness": 0.0,
            },
            "recommended_mood": "마음의 평화",
        }
