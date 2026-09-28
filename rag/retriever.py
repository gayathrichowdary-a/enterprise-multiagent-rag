# rag/retriever.py

def compute_rrf_relevance(dense_rankings, sparse_rankings, k=60, w_dense=0.7, w_sparse=0.3):
    rrf_scores = {}
    
    # Rank position loop for Dense Vector Search
    for rank, doc_id in enumerate(dense_rankings, start=1):
        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = 0.0
        # Formula: w_dense / (k + rank)
        rrf_scores[doc_id] += w_dense / (k + rank)
        
    # Rank position loop for Sparse BM25 Keyword Search
    for rank, doc_id in enumerate(sparse_rankings, start=1):
        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = 0.0
        # Formula: w_sparse / (k + rank)
        rrf_scores[doc_id] += w_sparse / (k + rank)
        
    return rrf_scores


def compute_combined_score(rrf_score, reliability_score=85.0, alpha=0.70, beta=0.30):
    # Normalize RRF score to 0-100 scale for parity with reliability
    normalized_rrf_score = min(100.0, rrf_score * 3000.0)
    
    # Combined Score Formula
    final_score = (alpha * normalized_rrf_score) + (beta * reliability_score)
    return round(final_score, 2)


def retrieve_docs(vector_db, query, k=3):
    if vector_db is None:
        return []
    docs = vector_db.similarity_search(query, k=k)
    return docs


def retrieve_hybrid_rrf_docs(vector_db, bm25_index, all_docs, query, k=3, reliability_scores=None):
    if vector_db is None:
        return []
        
    dense_docs = vector_db.similarity_search(query, k=k * 2)
    dense_ids = [doc.page_content for doc in dense_docs]
    
    sparse_ids = []
    if bm25_index and all_docs:
        tokenized_query = query.lower().split()
        sparse_docs = bm25_index.get_top_n(tokenized_query, all_docs, n=k * 2)
        sparse_ids = [doc.page_content for doc in sparse_docs]
    else:
        sparse_ids = dense_ids
        
    rrf_scores = compute_rrf_relevance(dense_ids, sparse_ids, k=60, w_dense=0.7, w_sparse=0.3)
    
    combined_scores = {}
    for content, r_score in rrf_scores.items():
        doc_rel = reliability_scores.get(content, 85.0) if reliability_scores else 85.0
        combined_scores[content] = compute_combined_score(r_score, doc_rel, alpha=0.70, beta=0.30)

    sorted_content = sorted(combined_scores.keys(), key=lambda x: combined_scores[x], reverse=True)[:k]
    
    fused_docs = []
    for doc in dense_docs:
        if doc.page_content in sorted_content and doc not in fused_docs:
            fused_docs.append(doc)
            
    return fused_docs if fused_docs else dense_docs[:k]


def get_context(docs):
    context = ""

    for item in docs:
        if isinstance(item, tuple):
            name, doc = item
            context += f"[SOURCE: {name}]\n"
        else:
            doc = item

        if hasattr(doc, "page_content"):
            context += doc.page_content
        else:
            context += str(doc)

        context += "\n\n"

    return context
