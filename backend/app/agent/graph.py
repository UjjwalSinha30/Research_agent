from langgraph.graph import StateGraph, encode
from app.agent.state import AgentState
from app.agent.nodes import (
    planner_node,
    search_node,
    scraper_node,
    retriever_node,
    synthesizer_node
)


def build_graph():
    graph = StateGraph(AgentState)

    # add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("scraper", scraper_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("synthesizer", synthesizer_node)
    
    # define flow
    graph.set_entry_point("planner")
    graph.add_edge("planner", "search")
    graph.add_edge("search", "scraper")
    graph.add_edge("scraper", "retriever")
    graph.add_edge("retriever", "synthesizer")
    graph.set_finish_point("synthesizer", END)
    
    return graph.compile()


# compiled graph instance
agent_graph = build_graph()

def run_agent(task_id: int, topic: str, user_id: int) -> dict:
    """Entry point called by Celery task."""
    initial_state = AgentState(
        task_id=task_id,
        user_id=user_id,
        topic=topic,
        sub_questions=[],
        search_results=[],
        scraped_content=[],
        retrieved_docs=[],
        agent_steps=[],
        content="",
        sources=[]
    )

    final_state = agent_graph.invoke(initial_state)
    return {
        "content": final_state["content"],
        "sources": final_state["sources"],
        "agent_steps": final_state["agent_steps"]
    }