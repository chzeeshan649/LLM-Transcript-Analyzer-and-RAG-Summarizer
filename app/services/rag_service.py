from typing import List, Dict, Any
from app.services.vectorstore_service import VectorStoreService
from app.services.firestore_client import FirestoreClient
from app.core.config import settings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI  
from langchain_core.prompts import ChatPromptTemplate


PROMPT = ChatPromptTemplate.from_template(
    """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, say that you don't know.
Summarize your answer in approximately 100 words.
Keep the answer clear and concise.

Question: {question}

Context:
{context}
"""
)


def _secs_to_hms(secs: int) -> str:
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


async def answer_query(
    user_id: str,
    transcript_id: str,
    question: str,
    top_k: int = 4,
    use_cache: bool = True,
) -> Dict[str, Any]:
    # Get retriever for this transcript
    retriever = await VectorStoreService.get_retriever(user_id, transcript_id, k=top_k)
    
    llm = ChatOpenAI(model=settings.OPENAI_CHAT_MODEL, temperature=0)
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )

    # Run the query
    out = await qa.ainvoke({"query": question})

    # Extract answer
    answer_text = out.get("result") or out.get("answer") or "I don't know"

    # Prepare parallel lists for timestamps and source_chunks
    timestamps: List[Dict[str, str]] = []
    source_chunks: List[str] = []

    source_docs = out.get("source_documents", [])
    for d in source_docs:
        meta = getattr(d, "metadata", {}) or {}
        start = int(meta.get("start", 0) or 0)
        end = int(meta.get("end", start) or start)
        timestamps.append({"start": _secs_to_hms(start), "end": _secs_to_hms(end)})
        source_chunks.append(d.page_content)

    result = {
        "answer": answer_text,
        "timestamps": timestamps,
        "source_chunks": source_chunks,
    }

    # Save query history under user-scoped document
    await FirestoreClient.save_query(user_id, transcript_id, result)
    return result


async def get_history(user_id: str, transcript_id: str):
    client = FirestoreClient._client_sync()
    qcol = (
        client.collection("users")
        .document(user_id)
        .collection("transcripts")
        .document(transcript_id)
        .collection("queries")
    )
    docs = [d.to_dict() for d in qcol.stream()]
    return docs
