from typing import TypedDict, Optional, List, Any


class AgentState(TypedDict):
    """LangGraph 워크플로우 공유 상태"""
    session_id: str
    survey_id: int
    survey_answers: dict
    callback_url: str
    emotion_result: Optional[dict]
    content_results: Optional[List[dict]]
    current_step: str
    error: Optional[str]
