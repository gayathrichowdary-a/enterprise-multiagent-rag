# dashboard/source_rankings.py
import streamlit as st

def source_rankings_page():
    st.title("📊 Enterprise Source Reliability & Quality Dashboard")
    st.caption("Real-time monitoring of document authority tiers, retrieval frequency, and adaptive trust scores.")

    sources = st.session_state.get("knowledge_sources", {})

    if not sources:
        st.info("📂 No enterprise sources registered yet. Please upload documents in the 'Upload Documents' tab first.")
        return

    # Top KPI Metrics Cards
    total_sources = len(sources)
    tier1_count = sum(1 for s in sources.values() if "Tier 1" in s.get("authority_tier", ""))
    avg_trust = sum(s.get("reliability_score", 80.0) for s in sources.values()) / max(1, total_sources)

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
        key=lambda item: item[1].get("reliability_score", 80.0), 
        reverse=True
    )

    for rank, (doc_name, data) in enumerate(sorted_sources, 1):
        rel_score = data.get("reliability_score", 80.0)
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
                st.caption(f"🏢 Dept: `{dept}` | 🛡️ `{tier.split(' ')[0]}` | Status: **{badge}**")
                st.caption(f"Adaptive Feedback: 👍 `{pos}` positive | 👎 `{neg}` negative penalties")
                
            with c_score:
                st.write(f"**Reliability Score: {rel_score:.1f}%**")
                st.progress(min(1.0, max(0.0, rel_score / 100.0)))
                
            st.divider()