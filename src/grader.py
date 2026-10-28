from langchain_core.prompts import ChatPromptTemplate
from .llm import get_llm

GRADER_PROMPT = ChatPromptTemplate.from_template(
    """You are a relevance grader. Your job is to decide whether retrieved documents
are genuinely relevant to the user's question.

Rules:
- Only answer "yes" or "no" (one word, nothing else).
- Answer "yes" ONLY if the documents contain information that directly helps answer the question.
- Answer "no" if:
  - The documents are about a completely different topic than the question.
  - The question is vague, conversational, or a greeting (e.g., "hi", "what is this", "thanks").
  - The documents only share a few keywords but don't actually address the question.

Question: {question}
Documents: {documents}
Relevant (yes/no):"""
)

def grade_relevance(question, documents):
    # Vague or conversational queries should always go to web search
    vague_patterns = [
        "what is this", "what's this", "hi", "hello", "thanks", "thank you",
        "ok", "okay", "bye", "help", "yes", "no", "hmm", "huh",
    ]
    q_lower = question.strip().lower().rstrip("?.! ")
    if q_lower in vague_patterns or len(q_lower) < 5:
        return "no"

    if not documents:
        return "no"

    doc_text = "\n".join([d.page_content[:600] for d in documents[:3]])
    llm = get_llm(0)
    res = (GRADER_PROMPT | llm).invoke({"question": question, "documents": doc_text})
    return "yes" if "yes" in res.content.strip().lower() else "no"