import logging

from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.graph.nodes import emotion_analyzer_node, content_searcher_node

logger = logging.getLogger(__name__)


def create_workflow():
    """LangGraph 워크플로우 생성

    Graph Edge가 오케스트레이션(Supervisor) 역할:
    START → emotion_analyzer → content_searcher → END
    """
    workflow = StateGraph(AgentState)

    # 노드 등록
    workflow.add_node("emotion_analyzer", emotion_analyzer_node)
    workflow.add_node("content_searcher", content_searcher_node)

    # Edge 연결 = 실행 순서 정의 (= Supervisor 역할)
    workflow.add_edge(START, "emotion_analyzer")
    workflow.add_edge("emotion_analyzer", "content_searcher")
    workflow.add_edge("content_searcher", END)

    compiled = workflow.compile()
    logger.info("LangGraph 워크플로우 컴파일 완료")
    return compiled


# 싱글톤 워크플로우 인스턴스
agent_workflow = create_workflow()
