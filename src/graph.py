from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.documents import Document
from .vector_store import load_vectorstore
from .grader import grade_relevance
from .llm import get_llm
from .web_search import web_search
from langchain_core.prompts import ChatPromptTemplate

class GraphState(TypedDict):
    question: str
    documents: List[Document]
    web_docs: List[Document]
    rewritten_query: str
    answer: str
    relevance: str

def retrieve_node(state: GraphState):
    db = load_vectorstore()
    if not db:
        return {"documents": []}
    docs = db.similarity_search(state["question"], k=4)
    return {"documents": docs}

def grade_node(state: GraphState):
    grade = grade_relevance(state["question"], state["documents"])
    return {"relevance": grade}

def rewrite_node(state: GraphState):
    llm = get_llm(0)
    prompt = ChatPromptTemplate.from_template("Rewrite this question for web search to be more specific: {question}")
    rewritten = (prompt | llm).invoke({"question": state["question"]})
    return {"rewritten_query": rewritten.content}

def web_search_node(state: GraphState):
    query = state.get("rewritten_query") or state["question"]
    docs = web_search(query)
    return {"web_docs": docs}

def generate_node(state: GraphState):
    llm = get_llm(0.2)
    all_docs = state["documents"] + state.get("web_docs", [])
    context = "\n\n".join([d.page_content for d in all_docs[:4]])
    prompt = ChatPromptTemplate.from_template(
        "Answer the question based on context:\nContext: {context}\nQuestion: {question}\nAnswer:"
    )
    answer = (prompt | llm).invoke({"context": context, "question": state["question"]})
    return {"answer": answer.content}

def decide_next(state: GraphState):
    if state["relevance"] == "yes":
        return "generate"
    else:
        return "rewrite"

workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade", grade_node)
workflow.add_node("rewrite", rewrite_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade")
workflow.add_conditional_edges("grade", decide_next, {"generate": "generate", "rewrite": "rewrite"})
workflow.add_edge("rewrite", "web_search")
workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

def run_agentic_rag(question: str):
    return app.invoke({"question": question, "documents":[], "web_docs":[], "rewritten_query":"", "answer":"", "relevance":""})