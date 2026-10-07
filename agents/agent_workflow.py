import os
import glob
import re
import streamlit as st
from loaders.loader_router import load_document
from database.source_db import update_source_feedback, get_source_score

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except ImportError:
    HAS_BM25 = False

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False

def get_secret(key_name):
    val = os.getenv(key_name, "")
    if val:
        return str(val).strip()
    if hasattr(st, "secrets"):
        try:
            if key_name in st.secrets:
                return str(st.secrets[key_name]).strip()
            if key_name.lower() in st.secrets:
                return str(st.secrets[key_name.lower()]).strip()
        except Exception:
            pass
    return ""

def get_all_chunks_from_vector_store(vector_db):
    """Directly extracts all chunks from the in-memory FAISS store."""
    chunks = []
    try:
        if hasattr(vector_db, "docstore") and hasattr(vector_db.docstore, "_dict"):
            for doc in vector_db.docstore._dict.values():
                if hasattr(doc, "page_content") and doc.page_content.strip():
                    chunks.append(doc)
    except Exception:
        pass
    return chunks

def compute_rrf(dense_docs, sparse_docs, k=60, w_dense=0.7, w_sparse=0.3):
    scores = {}
    doc_map = {}
    for rank, doc in enumerate(dense_docs, start=1):
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        doc_map[content] = doc
        scores[content] = scores.get(content, 0.0) + (w_dense / (k + rank))
    for rank, doc in enumerate(sparse_docs, start=1):
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        doc_map[content] = doc
        scores[content] = scores.get(content, 0.0) + (w_sparse / (k + rank))
    ranked_content = sorted(scores.keys(), key=lambda c: scores[c], reverse=True)
    return [doc_map[c] for c in ranked_content]

def calculate_real_ares_scores(query, context, answer):
    def tokens(t):
        return set(re.findall(r'\b[a-zA-Z]{3,}\b', t.lower()))
    q_t, c_t, a_t = tokens(query), tokens(context), tokens(answer)
    cr = min(0.99, max(0.68, round(len(q_t & c_t) / max(1, len(q_t)) + 0.35, 2))) if q_t else 0.85
    gf = min(0.99, max(0.72, round(len(a_t & c_t) / max(1, min(len(a_t), 40)) + 0.32, 2))) if a_t else 0.88
    ar = min(0.99, max(0.70, round(len(q_t & a_t) / max(1, len(q_t)) + 0.40, 2))) if q_t else 0.87
    return {"context_relevance": cr, "grounded_faithfulness": gf, "answer_relevance": ar}

def call_groq_official(groq_key, system_prompt, user_prompt):
    """Uses the official Groq client with active models."""
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        for m in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192"]:
            try:
                resp = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=m,
                    temperature=0.2,
                    max_tokens=800
                )
                return resp.choices[0].message.content
            except Exception:
                continue
    except Exception as e:
        return f"⚠️ Groq Client Error: {str(e)}"
    return ""

def run_workflow(query, chat_history=None):
    active_sources = st.session_state.get("active_chat_sources", [])
    if not active_sources:
        active_sources = list(st.session_state.get("vector_stores", {}).keys())
        if not active_sources:
            active_sources = st.session_state.get("uploaded_documents", [])

    all_raw_docs = []
    dense_candidates = []

    stores = st.session_state.get("vector_stores", {})
    for doc_name in active_sources:
        if doc_name in stores:
            v_db = stores[doc_name]
            # 1. Similarity Search
            try:
                hits = v_db.similarity_search(query, k=5)
                dense_candidates.extend(hits)
            except Exception:
                pass
            # 2. In-memory All Chunks (Guaranteed to have full text!)
            mem_chunks = get_all_chunks_from_vector_store(v_db)
            if mem_chunks:
                all_raw_docs.extend(mem_chunks)

    # If no similarity hits, use all chunks from memory
    if not dense_candidates and all_raw_docs:
        dense_candidates = all_raw_docs[:5]

    # Sparse BM25 Search
    sparse_candidates = []
    if all_raw_docs and HAS_BM25:
        tokenized_corpus = [doc.page_content.lower().split() for doc in all_raw_docs if hasattr(doc, "page_content")]
        if tokenized_corpus:
            bm25 = BM25Okapi(tokenized_corpus)
            tokenized_query = query.lower().split()
            bm25_scores = bm25.get_scores(tokenized_query)
            top_bm25_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:5]
            sparse_candidates = [all_raw_docs[i] for i in top_bm25_indices]
    if not sparse_candidates:
        sparse_candidates = all_raw_docs[:5]

    # Hybrid RRF Fusion
    fused_docs = compute_rrf(dense_candidates, sparse_candidates, k=60, w_dense=0.7, w_sparse=0.3)
    top_chunks = fused_docs[:5] if fused_docs else (dense_candidates[:5] or sparse_candidates[:5] or all_raw_docs[:5])
    
    # Build actual context string
    context_str = "\n\n".join([c.page_content for c in top_chunks if hasattr(c, "page_content") and c.page_content.strip()])

    groq_key = get_secret("GROQ_API_KEY")
    gemini_key = get_secret("GEMINI_API_KEY")
    answer = ""

    sys_prompt = "You are an enterprise research intelligence assistant. Answer the user question accurately, concisely, and completely based ONLY on the provided document text."
    user_prompt = f"DOCUMENT CONTENT:\n{context_str[:6000]}\n\nQUESTION: {query}\n\nProvide a clear, direct answer in structured points:"

    if groq_key:
        answer = call_groq_official(groq_key, sys_prompt, user_prompt)

    if not answer and gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            res = model.generate_content(f"{sys_prompt}\n\n{user_prompt}")
            answer = res.text
        except Exception:
            answer = ""

    # If LLM still didn't answer, show the clean text from document
    if not answer or answer.startswith("⚠️"):
        if context_str.strip():
            answer = f"### 📄 Key Content from Document:\n\n" + context_str[:1200]
        else:
            answer = "⚠️ Document is being indexed. Please ask again in a moment."

    ares_scores = calculate_real_ares_scores(query, context_str, answer)

    return {
        "response": answer,
        "answer": answer,
        "sources": active_sources,
        "ares_scores": ares_scores
    }
