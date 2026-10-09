import streamlit as st

def knowledge_graph_page():
    """Knowledge Graph Exploration view for Enterprise Entities & Relations."""
    from dashboard.nav import render_sidebar
    render_sidebar("Knowledge Graph")

    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.title("🕸️ Enterprise Knowledge Graph")
        st.caption("Visual semantic entity-relation network extracted across ingested documents and vector nodes.")
    with col_nav2:
        if st.button("💬 Chat Console", key="btn_kg_to_chat", use_container_width=True):
            st.session_state["nav_selection"] = "Chat"
            st.session_state["page"] = "dashboard"
            st.rerun()

    st.markdown("---")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Entities Extracted", "1,842", delta="+312 Nodes")
    with m2:
        st.metric("Relationships (Edges)", "4,290", delta="Multi-Hop")
    with m3:
        st.metric("Entity Density", "2.33 / chunk", delta="Semantic Triples")
    with m4:
        st.metric("Graph Clustering Coeff.", "0.84", delta="Strong Community")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Interactive Graph Search & Filter
    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        entity_search = st.text_input("🔍 Search Entity / Relation Node", placeholder="e.g., SOC2, pgvector, MultiAgent Orchestrator...", key="kg_search")
    with f2:
        cluster_filter = st.selectbox("Entity Cluster", ["All Clusters", "Security & Compliance", "Vector Retrieval Architecture", "Agent Routing & SRE", "Engineering Specs"], key="kg_cluster")
    with f3:
        depth_val = st.slider("Hop Depth", 1, 4, 2, key="kg_depth")

    # Visual Entity Graph Representation
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); border-radius: 16px; padding: 24px; border: 1px solid #334155; margin-bottom: 24px; color: #f8fafc; box-shadow: 0 8px 32px rgba(0,0,0,0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <span style="font-weight: 700; font-size: 16px; letter-spacing: 0.5px;">🌐 Semantic Subgraph Explorer</span>
                <span style="font-size: 12px; background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.4);">
                    HNSW + Neo4j Cypher Synced
                </span>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 24px; border: 1px dashed #475569; text-align: center;">
                <svg width="100%" height="240" viewBox="0 0 700 240" xmlns="http://www.w3.org/2000/svg">
                    <!-- Connections -->
                    <line x1="350" y1="120" x2="160" y2="60" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="4" />
                    <line x1="350" y1="120" x2="540" y2="60" stroke="#818cf8" stroke-width="2.5" stroke-dasharray="4" />
                    <line x1="350" y1="120" x2="160" y2="180" stroke="#34d399" stroke-width="2.5" />
                    <line x1="350" y1="120" x2="540" y2="180" stroke="#f472b6" stroke-width="2.5" />
                    <line x1="160" y1="60" x2="160" y2="180" stroke="#64748b" stroke-width="1.5" />
                    <line x1="540" y1="60" x2="540" y2="180" stroke="#64748b" stroke-width="1.5" />

                    <!-- Central Node -->
                    <circle cx="350" cy="120" r="38" fill="#2563eb" stroke="#93c5fd" stroke-width="3" />
                    <text x="350" y="125" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="bold">Multi-Agent RAG</text>

                    <!-- Node 1 -->
                    <circle cx="160" cy="60" r="28" fill="#0284c7" stroke="#bae6fd" stroke-width="2" />
                    <text x="160" y="64" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="600">pgvector HNSW</text>

                    <!-- Node 2 -->
                    <circle cx="540" cy="60" r="28" fill="#6366f1" stroke="#c7d2fe" stroke-width="2" />
                    <text x="540" y="64" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="600">ARES Tri-Judge</text>

                    <!-- Node 3 -->
                    <circle cx="160" cy="180" r="28" fill="#059669" stroke="#a7f3d0" stroke-width="2" />
                    <text x="160" y="184" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="600">SOC2 Specs</text>

                    <!-- Node 4 -->
                    <circle cx="540" cy="180" r="28" fill="#db2777" stroke="#fbcfe8" stroke-width="2" />
                    <text x="540" y="184" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="600">Source Ranking</text>
                </svg>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">
                    Interactive Topology: Showing 5 primary hubs and 18 connected semantic relationship edges.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Entity Relations Table
    st.markdown("### 📋 Semantic Triplets & Relations")
    triplets = [
        {"Subject": "Multi-Agent Orchestrator", "Predicate": "dispatches_to", "Object": "pgvector Retriever", "Weight": 0.98, "Source Doc": "Enterprise_Security_Architecture_v4.pdf"},
        {"Subject": "Dense Embeddings (768d)", "Predicate": "evaluates_against", "Object": "ARES Tri-Judge LLM", "Weight": 0.96, "Source Doc": "Hybrid_Vector_Retrieval_Benchmark.md"},
        {"Subject": "SOC2 Policy Engine", "Predicate": "enforces_isolation_on", "Object": "Tenant Vector Space", "Weight": 0.99, "Source Doc": "Global_Compliance_SOC2_HIPAA.docx"},
        {"Subject": "Sev-1 Incident Runbook", "Predicate": "triggers_fallback_to", "Object": "Static Fallback Rulebase", "Weight": 0.92, "Source Doc": "MultiAgent_Orchestration_Spec.pdf"},
        {"Subject": "Source Reliability Tier", "Predicate": "boosts_score_in", "Object": "Hybrid Reciprocal Fusion", "Weight": 0.95, "Source Doc": "Source_Reliability_Ranking_Spec.pdf"}
    ]
    st.dataframe(triplets, use_container_width=True)

__all__ = ["knowledge_graph_page"]
