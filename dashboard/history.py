import streamlit as st

def history_page():
    """Historical Execution Logs, Audit Trail, and Past Queries."""
    from dashboard.nav import render_sidebar
    render_sidebar("History")

    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.title("📜 Query History & Audit Trail")
        st.caption("Complete enterprise audit trail of queries, retrieved citations, and user feedback logs.")
    with col_nav2:
        if st.button("💬 Chat Console", key="btn_hist_to_chat", use_container_width=True):
            st.session_state["nav_selection"] = "Chat"
            st.session_state["page"] = "dashboard"
            st.rerun()

    st.markdown("---")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Queries Logged", "148", delta="+12 Today")
    with m2:
        st.metric("Avg Latency", "342 ms", delta="-45 ms")
    with m3:
        st.metric("Positive User Feedback", "96.2%", delta="👍 High Satisfaction")
    with m4:
        st.metric("Audit Compliance", "100%", delta="SOC2 Type II")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Search and Filter
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_input("🔍 Filter Past Queries", placeholder="Search by query term, document name, or agent tag...", key="hist_filter")
    with c2:
        st.selectbox("Filter Status", ["All Results", "High Confidence (>90%)", "Flagged for Review"], key="hist_status")

    # Query History Table
    history_records = [
        {
            "Timestamp": "2026-10-09 10:14:22",
            "Query": "What are the SOC2 security protocols and vector encryption requirements?",
            "Agent Mode": "Adaptive Multi-Agent",
            "Top Source": "Enterprise_Security_Architecture_v4.pdf",
            "ARES Faithfulness": "98.2%",
            "Latency": "310 ms",
            "User Feedback": "👍 Helpful"
        },
        {
            "Timestamp": "2026-10-09 09:41:05",
            "Query": "Explain the multi-agent microservices and pgvector retrieval pipeline",
            "Agent Mode": "Hybrid Dense + Sparse",
            "Top Source": "MultiAgent_Orchestration_Spec.pdf",
            "ARES Faithfulness": "97.4%",
            "Latency": "385 ms",
            "User Feedback": "👍 Helpful"
        },
        {
            "Timestamp": "2026-10-08 16:30:11",
            "Query": "What are the Sev-1 incident escalation and on-call procedures?",
            "Agent Mode": "Direct Dense Vector",
            "Top Source": "Q3_Infrastructure_SLA_CostReport.csv",
            "ARES Faithfulness": "95.8%",
            "Latency": "260 ms",
            "User Feedback": "👍 Helpful"
        },
        {
            "Timestamp": "2026-10-08 14:12:48",
            "Query": "Compare dense vs sparse hybrid ranking performance across enterprise datasets",
            "Agent Mode": "Adaptive Multi-Agent",
            "Top Source": "Hybrid_Vector_Retrieval_Benchmark.md",
            "ARES Faithfulness": "99.0%",
            "Latency": "420 ms",
            "User Feedback": "👍 Helpful"
        }
    ]
    st.dataframe(history_records, use_container_width=True)

    st.markdown("---")
    col_exp1, col_exp2 = st.columns([1, 4])
    with col_exp1:
        if st.button("📥 Export Audit Log (CSV)"):
            st.toast("Exported 148 audit logs to CSV.")
    with col_exp2:
        if st.button("🗑️ Clear Past Session Queries"):
            st.toast("Current session query cache cleared.")

__all__ = ["history_page"]
