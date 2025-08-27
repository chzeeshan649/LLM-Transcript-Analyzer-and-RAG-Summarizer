# LLM Transcript Analyzer + RAG Summarizer

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.110-green)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-v1.0-orange)](https://www.langchain.com/)

---

## Overview

**LLM Transcript Analyzer + RAG Summarizer** is a FastAPI backend service that allows users to:

- Upload pre-transcribed text files (lectures, podcasts, etc.) with timestamps.
- Automatically chunk transcripts and generate embeddings.
- Perform semantic querying using Retrieval-Augmented Generation (RAG) with LangChain and OpenAI.
- Return AI-generated answers with **timestamps** and **source excerpts**.
- Keep all user data scoped and stored per user in Firestore.

---

## Features

- **Transcript Upload & Indexing**  
  - Accepts plain text transcript files with timestamps.
  - Chunks transcript into token-aware segments.
  - Generates embeddings (OpenAI or HuggingFace) for semantic search.
  - Stores embeddings in FAISS vectorstore.

- **Semantic Q&A with RAG**  
  - Accepts user queries and retrieves relevant chunks.
  - Uses OpenAI LLM (e.g., GPT-4) to answer based on transcript.
  - Returns answer, timestamps, and source chunks.

- **User Access Control**  
  - Each user can only see their transcripts and query history.
  - Queries and history stored per user in Firestore.

- **Caching / History**  
  - Optional caching to avoid repeated LLM calls.
  - Persistent query history in Firestore.

---

## Tech Stack

- **Backend**: FastAPI  
- **Database**: Firestore (Google Cloud)  
- **Vector Store**: FAISS (in-memory, optional persistence)  
- **Embeddings**: OpenAI / HuggingFace  
- **LLM**: OpenAI GPT-4 / GPT-3.5  
- **RAG Framework**: LangChain  
- **Containerization**: Docker  

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/llm-transcript-rag.git
cd llm-transcript-rag 
```
### 2. Set up environment variables
Create a .env file in the root directory:
### 3. Run with Docker 🐳

```bash
docker build -t transcript-rag .
docker run -d -p 8000:8000 --env-file .env -v $(pwd)/service-account.json:/app/service-account.json transcript-rag
```
Now open 👉 http://localhost:8000/docs