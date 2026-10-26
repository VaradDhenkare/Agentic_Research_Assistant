from langchain_core.prompts import ChatPromptTemplate
from .llm import get_llm
prompt = ChatPromptTemplate.from_template("Question: {question}\nDocs: {documents}\nRelevant? yes/no:")
def grade_relevance(question, documents):
    if not documents: return "no"
    doc_text = "\n".join([d.page_content[:800] for d in documents[:2]])
    llm = get_llm(0)
    res = (prompt | llm).invoke({"question": question, "documents": doc_text})
    return "yes" if "yes" in res.content.lower() else "no"