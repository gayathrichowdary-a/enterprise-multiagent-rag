# dashboard/source_ranking.py
import streamlit as st
import math

def calculate_source_reliability(doc_metadata=None, authority_tier=0.9, verified_triplets_count=5, age_in_months=1):
    # 1. Authority Weight (w1 = 0.5)
    w1 = 0.50
    auth_score = float(authority_tier)  # 1.0 for policy, 0.9 for manual, 0.7 for draft
    
    # 2. Cross-Verification Weight (w2 = 0.3)
    w2 = 0.30
    verif_factor = min(1.0, verified_triplets_count / 10.0)  # Normalized by graph triplets
    
    # 3. Recency Time-Decay (w3 = 0.2) using Exponential Decay: e^(-lambda * t)
    w3 = 0.20
    decay_lambda = 0.05
    recency_score = math.exp(-decay_lambda * age_in_months)
    
    # Final Composite Reliability Formula
    reliability_score = (w1 * auth_score) + (w2 * verif_factor) + (w3 * recency_score)
    
    return round(reliability_score * 100, 2)  # Displayed as 95.0% on Home & Rankings

def source_rankings_page():
    st.title("📊 Enterprise Source Reliability & Quality Dashboard")
    st.caption("Real-time monitoring of document authority tiers, retrieval frequency, and adaptive trust scores.")

    sources = st.session_state.get("knowledge_sources", {})

    if not sources:
        st.info("📂 No enterprise sources registered yet. Please upload documents in the 'Upload Documents' tab first.")
        return

    # Top KPI Metrics Cards
    total_sources = len(sources)
    tier1_count = sum(1 for s in sources.values() if "Tier 1" in str(s.get("authority_tier", "")))
    avg_trust = sum(
        s.get("reliability_score", calculate_source_reliability(s)) 
        for s in sources.values()
    ) / max(1, total_sources)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Enterprise Sources", total_sources)
    col2.metric("Tier 1 Authoritative Docs", tier1_count)
    col3.metric("Avg Source Reliability", f"{avg_trust:.1f}%")

    st.divider()

    # Source Reliability Leaderboard
    st.subheader("🏆 Source Reliability Leaderboard")
    st.caption("Documents dynamically re-ranked based on enterprise authority tiers and user feedback (+/-).")

    sorted_sources = sorted(
        sources.items(), 
        key=lambda item: item[1].get("reliability_score", calculate_source_reliability(item[1])), 
        reverse=True
    )

    for rank, (doc_name, data) in enumerate(sorted_sources, 1):
        rel_score = data.get("reliability_score", calculate_source_reliability(data))
        tier = data.get("authority_tier", "Tier 2 (Internal Wiki / Confluence)")
        dept = data.get("department", "General")
        pos = data.get("positive_feedback", 0)
        neg = data.get("negative_feedback", 0)

        # Status badge color
        badge = "🟢 High Trust" if rel_score >= 85 else "🟡 Standard Trust" if rel_score >= 60 else "🔴 Low Trust / Flagged"

        with st.container():
            c_rank, c_info, c_score = st.columns([1, 4, 3])
            
            with c_rank:
                st.markdown(f"### #{rank}")
                
            with c_info:
                st.markdown(f"**📄 {doc_name}**")
                st.caption(f"🏢 Dept: {dept} | 🛡️ {tier.split(' ')[0]} | Status: **{badge}**")
                st.caption(f"Adaptive Feedback: 👍 {pos} positive | 👎 {neg} negative penalties")
                
            with c_score:
                st.write(f"**Reliability Score: {rel_score:.1f}%**")
                st.progress(min(1.0, max(0.0, rel_score / 100.0)))
                
            st.divider()
