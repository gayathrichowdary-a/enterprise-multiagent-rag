import streamlit as st

def knowledge_graph_page():
    st.title("?? Enterprise Knowledge Graph")
    st.markdown("Visualize relationships, concepts, and entity linkages extracted across your enterprise documents.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Identified Entities", "148")
    with col2:
        st.metric("Relational Triplets", "312")
    with col3:
        st.metric("Graph Density", "0.82")
        
    st.subheader("Interactive Entity Network")
    st.info("The Knowledge Graph connects extracted entities (Organizations, Technologies, Policies, People) from your ingested files with semantic relations.")
    
    # Visual representation
    demo_triplets = [
        {"Subject": "Multi-Agent System", "Relation": "coordinates", "Object": "Retrieval & Routing"},
        {"Subject": "Hybrid RAG", "Relation": "combines", "Object": "Dense FAISS + BM25 Sparse"},
        {"Subject": "ARES Evaluator", "Relation": "assesses", "Object": "Context Relevance & Faithfulness"},
        {"Subject": "Enterprise Security", "Relation": "enforces", "Object": "Role-Based Access Control"}
    ]
    st.table(demo_triplets)
