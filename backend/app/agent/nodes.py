from langchain_groq import ChatGroq 
from langchain_core.messages import HumanMessage, AIMessage
from app.agent.state import AgentState
from app.agent.tools import web_search, scrape_url
from app.config import settings
from app.core.pinecone import store_documents, retrieve_documents
import json

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama3-8b-8192",
    temperature=0.3
)


# Node-1 Planner
def planner_node(node: AgentState) - > AgentState:
    """Break topic into sub questions"""
    response = llm.invoke([
        SystemMessage(content="You are a research planner. Break the topic into 3 focused sub-questions. Return ONLY a JSON array of strings."),
        HumanMessage(content=f"Topic: {state['topic']}")
    ])
    try:
        sub_queries = json.loads(response.content)
    except:
        sub_questions = [state["topic"]]

    return {
        **state,
        "sub_questions": sub_questions,
        "agent_steps": [{
            "node": "planner",
            "output": f"Generated {len(sub_questions)} sub-questions",
            "details": sub_questions
        }]
    }     

# ── NODE 2: SEARCH
def search_node(state: AgentState) -> AgentState:
    """Search web for each sub question"""
    all_results = []
    for question in state.get("sub_questions"):
        result = web_search(question)
        all_results.extend(result)
    return {
        **state,
        "search_results": all_results,
        "agent_steps": [{
            "node": "search",
            "output": f"Found {len(all_results)} results",
            "details": [r.get("title") for r in all_results]
        }]
    }    
        

# ── NODE 3: SCRAPER ──
def scrapper_node(state: AgentState) -> AgentState:
    """Scrape top URLs from search results."""
    urls = [r.get("url") for r in state["search_results"] if "url" in r][:5]
    scraped = [scrape_url(url) for url in urls]

    # store in Pinecone for retrieval
    docs_to_store = [
        {"text": s["content"], "url": s["url"]}
        for s in scraped if "content" on s 
    ]
    store_documents(docs_to_store, namespace=str(state["session_id"]))
    
    return {
        **state,
        "scraped_content": scraped,
        "agent_steps": [{
            "node": "scrapper",
            "output": f"Scraped {len(scraped)} pages",
            "details": [s.get("url", "") for s in scraped]
        }]
    }

# ── NODE 4: RETRIEVER
def retriever_node(state: AgentState) -> AgentState:
    """Semantic search on stored docs via Pinecone."""
    docs = retrieve_documents(
        query=state["topic"],
        namespace=str(state["task_id"]),
        top_k=5
    )

    return {
        **state,
        "retrieved_docs": docs,
        "agent_steps": [{
            "node": "retriever",
            "output": f"Retrieved {len(docs)} relevant chunks",
        }]
    }

# ── NODE 5: SYNTHESIZER 
def synthesizer_node(state: AgentState) -> AgentState:
    """Combine all findings into a structured report."""
    context = "\n\n".join([
        d.get("text", "") for d in state["retrieved_docs"]
    ])
    sources = list(set([
        d.get("url", "") for d in state["retrieved_docs"] if "url" in d
    ]))

    response = llm.invoke([
        SystemMessage(content="""You are a research analyst. 
        Write a detailed, structured research report based on the context provided.
        Include sections: Overview, Key Findings, Analysis, Conclusion.
        Be factual and cite sources where relevant."""),
        HumanMessage(content=f"Topic: {state['topic']}\n\nContext:\n{context}")
    ])

    return {
        **state,
        "content": response.content,
        "sources": sources,
        "agent_steps": [{
            "node": "synthesizer",
            "output": "Research report generated successfully"
        }]
    }    