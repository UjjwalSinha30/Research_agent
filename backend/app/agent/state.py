from typing import TypeDict, Annotated
import operator

class AgentState(TypeDict):
    task_id: str
    user_id: int
    topic: str
    
    # each nodes append to these
    sub_questions: list[str]
    search_results: Annotated[List[str], operator.add]
    scraped_content: Annotated[List[str], operator.add]
    retrieved_docs: Annotated[List[str], operator.add]
    agent_steps: Annotated[List[str], operator.add]

    # final_output
    content: str
    sources: list[str]