# dashboard/graph_view.py
import streamlit as st

# Exact knowledge triples from your enterprise system
KNOWLEDGE_TRIPLES = [
    {"subject": "AI Medical Report Doc", "predicate": "specifies", "object": "Prompt Engineering Layer"},
    {"subject": "AI Medical Report Doc", "predicate": "defines", "object": "DFD Level 0 (Context)"},
    {"subject": "DFD Level 0 (Context)", "predicate": "decomposes into", "object": "DFD Level 1 (Report Upload)"},
    {"subject": "Prompt Engineering Layer", "predicate": "constructs prompt for", "object": "Gemini AI Analysis Engine"},
    {"subject": "Gemini AI Analysis Engine", "predicate": "produces response for", "object": "Response Parsing & Display"},
    {"subject": "Response Parsing & Display", "predicate": "renders into", "object": "Conversational Chatbot"},
    {"subject": "Conversational Chatbot", "predicate": "synchronizes with", "object": "Episodic & Profile Memory"},
    {"subject": "Gemini AI Analysis Engine", "predicate": "evaluated by", "object": "ARES Quality Verifier (PPI 95% CI)"},
    {"subject": "ARES Quality Verifier (PPI 95% CI)", "predicate": "grounds against", "object": "AI Medical Report Doc"},
    {"subject": "Episodic & Profile Memory", "predicate": "context feed to", "object": "Prompt Engineering Layer"}
]


def get_subgraph(query_text, hop_depth):
    """Filters triples based on keyword query and hop depth."""
    query = query_text.strip().lower()
    if not query or hop_depth == "Full Cluster View":
        return KNOWLEDGE_TRIPLES, None

    # Step 1: Find focal nodes containing the search keyword
    focal_nodes = set()
    for t in KNOWLEDGE_TRIPLES:
        for word in query.split():
            if word in t["subject"].lower():
                focal_nodes.add(t["subject"])
            if word in t["object"].lower():
                focal_nodes.add(t["object"])

    if not focal_nodes:
        return [], set()

    max_hops = 1 if "1-Hop" in hop_depth else 2
    current_nodes = set(focal_nodes)
    result_triples = []

    for _ in range(max_hops):
        next_nodes = set()
        for t in KNOWLEDGE_TRIPLES:
            s, o = t["subject"], t["object"]
            if s in current_nodes or o in current_nodes:
                if t not in result_triples:
                    result_triples.append(t)
                next_nodes.add(s)
                next_nodes.add(o)
        current_nodes = next_nodes

    return result_triples, focal_nodes


def graph_page():
    is_dark = st.session_state.get("ui_theme", "Light") == "Dark"

    # Theme colors
    graph_bg = "#090d16" if is_dark else "#f8fafc"
    edge_color = "#38bdf8" if is_dark else "#475569"
    default_node_fill = "#1e293b" if is_dark else "#ffffff"
    default_node_font = "#f1f5f9" if is_dark else "#1e293b"

    highlight_node_fill = "#2563eb" if is_dark else "#dbeafe"
    highlight_node_font = "#ffffff" if is_dark else "#1e40af"

    st.title("🕸️ Enterprise Knowledge Graph Explorer")
    st.caption("Traverse multi-hop entity relationships and inspect extracted subject-predicate-object knowledge triples.")

    col1, col2 = st.columns([3, 2])
    with col1:
        focus_entity = st.text_input(
            "🔍 Focus on Entity or Keyword",
            value=st.session_state.get("kg_search", ""),
            placeholder="Type 'Gemini', 'Prompt', 'ARES', or 'Medical' and press Enter...",
            key="input_focus_entity"
        )
    with col2:
        hop_depth = st.selectbox(
            "Sub-graph Hop Depth",
            ["Full Cluster View", "1-Hop (Direct Relations)", "2-Hop (Expanded Context)"],
            index=0 if not focus_entity else 1,
            key="select_hop_depth"
        )

    # Filter knowledge graph dynamically
    filtered_triples, focal_nodes = get_subgraph(focus_entity, hop_depth)

    st.write("")
    st.subheader("📊 Entity-Relationship Subgraph")

    if not filtered_triples:
        st.warning(f"No graph entities matched **'{focus_entity}'**. Try: **Gemini**, **Prompt**, **ARES**, or **DFD**.")
    else:
        # Collect distinct nodes in view
        nodes_in_view = set()
        for t in filtered_triples:
            nodes_in_view.add(t["subject"])
            nodes_in_view.add(t["object"])

        # Construct Graphviz DOT string
        dot = [
            "digraph G {",
            f'    bgcolor="{graph_bg}";',
            '    rankdir=LR;',
            '    node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10, penwidth=1.5];',
            f'    edge [fontname="Helvetica", fontsize=8, color="{edge_color}", fontcolor="{edge_color}"];'
        ]

        # Draw Nodes with Highlight for focal nodes
        for node in nodes_in_view:
            is_match = focal_nodes and (node in focal_nodes)
            fill = highlight_node_fill if is_match else default_node_fill
            font = highlight_node_font if is_match else default_node_font
            border = "#60a5fa" if is_match else "#94a3b8"
            penwidth = "2.5" if is_match else "1.0"
            dot.append(f'    "{node}" [fillcolor="{fill}", fontcolor="{font}", color="{border}", penwidth="{penwidth}"];')

        # Draw Directed Edges with predicate labels
        for t in filtered_triples:
            dot.append(f'    "{t["subject"]}" -> "{t["object"]}" [label=" {t["predicate"]} "];')

        dot.append("}")
        dot_code = "\n".join(dot)

        st.graphviz_chart(dot_code, use_container_width=True)

        if focus_entity.strip():
            st.success(f"🎯 Filtered subgraph: Showing **{len(nodes_in_view)} nodes** connected to **'{focus_entity}'** ({hop_depth}).")

    # -------------------------------------------------------------
    # Synced Triples Table
    # -------------------------------------------------------------
    st.write("")
    with st.expander("📜 View Extracted Knowledge Triples (Subject - Predicate - Object)", expanded=True):
        if filtered_triples:
            st.table(filtered_triples)
        else:
            st.write("No triples to display.")