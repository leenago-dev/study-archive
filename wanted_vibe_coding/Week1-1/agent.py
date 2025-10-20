"""
LangGraph 기반 웹 검색 에이전트
Tavily Search를 활용한 대화형 AI 에이전트
"""

from typing import Annotated, TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from config import settings


class AgentState(TypedDict):
    """에이전트 상태 정의"""

    messages: Annotated[List[BaseMessage], add_messages]


class WebSearchAgent:
    """웹 검색 기능을 갖춘 LangGraph 에이전트"""

    def __init__(self):
        """에이전트 초기화"""
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        self.graph = self._build_graph()

    def _initialize_llm(self) -> ChatOpenAI:
        """LLM 초기화"""
        return ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.temperature,
            openai_api_key=settings.openai_api_key,
            streaming=True,
        )

    def _initialize_tools(self) -> List:
        """도구 초기화 (Tavily Search)"""
        tavily_tool = TavilySearch(
            max_results=settings.tavily_max_results, api_key=settings.tavily_api_key
        )
        return [tavily_tool]

    def _build_graph(self) -> StateGraph:
        """LangGraph 그래프 구축"""
        # StateGraph 생성
        graph_builder = StateGraph(AgentState)

        # LLM에 도구 바인딩
        llm_with_tools = self.llm.bind_tools(self.tools)

        # 챗봇 노드 정의
        def chatbot(state: AgentState):
            """챗봇 노드: LLM 호출 및 응답 생성"""
            # 시스템 메시지 추가
            messages = state["messages"]
            if not any(isinstance(msg, SystemMessage) for msg in messages):
                system_message = SystemMessage(
                    content="""당신은 웹 검색 기능을 갖춘 유용한 AI 어시스턴트입니다.

사용자의 질문에 답변하기 위해:
1. 최신 정보가 필요한 경우 Tavily Search 도구를 사용하여 웹 검색을 수행하세요.
2. 검색 결과를 바탕으로 정확하고 유용한 답변을 제공하세요.
3. 검색 결과가 없어도 최선을 다해 답변하세요.
4. 한국어로 친절하게 답변하세요.

항상 사용자에게 도움이 되는 정보를 제공하는 것을 목표로 하세요."""
                )
                messages = [system_message] + messages

            # LLM 호출
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}

        # 노드 추가
        graph_builder.add_node("chatbot", chatbot)

        # 도구 노드 추가
        tool_node = ToolNode(tools=self.tools)
        graph_builder.add_node("tools", tool_node)

        # 엣지 추가
        graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,  # 도구 호출 여부 확인
        )
        graph_builder.add_edge("tools", "chatbot")  # 도구 실행 후 챗봇으로 복귀
        graph_builder.add_edge(START, "chatbot")  # 시작점에서 챗봇으로

        # 메모리 체크포인터 추가
        memory = InMemorySaver()

        # 그래프 컴파일
        return graph_builder.compile(checkpointer=memory)

    async def process_message(self, message: str, session_id: str = "default") -> str:
        """
        메시지 처리 및 응답 생성

        Args:
            message: 사용자 메시지
            session_id: 세션 ID (대화 히스토리 관리용)

        Returns:
            에이전트 응답 메시지
        """
        # 입력 상태 구성
        input_state = {"messages": [HumanMessage(content=message)]}

        # 설정 (세션 ID 포함)
        config = {"configurable": {"thread_id": session_id}}

        # 그래프 실행
        final_state = await self.graph.ainvoke(input_state, config=config)

        # 마지막 AI 메시지 추출
        messages = final_state["messages"]
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                return msg.content

        return "죄송합니다. 응답을 생성할 수 없습니다."

    async def stream_message(self, message: str, session_id: str = "default"):
        """
        메시지 처리 및 스트리밍 응답 생성

        Args:
            message: 사용자 메시지
            session_id: 세션 ID

        Yields:
            스트리밍 응답 청크
        """
        # 입력 상태 구성
        input_state = {"messages": [HumanMessage(content=message)]}

        # 설정 (세션 ID 포함)
        config = {"configurable": {"thread_id": session_id}}

        # 그래프 스트리밍 실행
        async for event in self.graph.astream_events(
            input_state, config=config, version="v2"
        ):
            # LLM 응답 토큰 스트리밍
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if hasattr(chunk, "content") and chunk.content:
                    yield chunk.content

    def get_conversation_history(self, session_id: str = "default") -> List[dict]:
        """
        대화 히스토리 조회

        Args:
            session_id: 세션 ID

        Returns:
            대화 히스토리 리스트
        """
        config = {"configurable": {"thread_id": session_id}}

        try:
            # 체크포인트에서 상태 가져오기
            state = self.graph.get_state(config)
            messages = state.values.get("messages", [])

            # 메시지를 딕셔너리 형태로 변환
            history = []
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    history.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    history.append({"role": "assistant", "content": msg.content})
                elif isinstance(msg, SystemMessage):
                    history.append({"role": "system", "content": msg.content})

            return history
        except Exception as e:
            print(f"히스토리 조회 오류: {e}")
            return []


# 싱글톤 에이전트 인스턴스
_agent_instance = None


def get_agent() -> WebSearchAgent:
    """에이전트 싱글톤 인스턴스 반환"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = WebSearchAgent()
        print("✅ 웹 검색 에이전트 초기화 완료")
    return _agent_instance
