import re
import datetime
import streamlit as st
from dashboard.upload import init_knowledge_base_state

try:
    from agents.agent_workflow import call_groq_llm, get_secret, build_context
    _LLM_ERR = ""
except Exception as e:
    call_groq_llm = get_secret = build_context = None
    _LLM_ERR = f"{type(e).__name__}: {e}"

_STOP = set("""about above after again against all also and any are because been before being below
between both but can could did does doing down during each few for from further had has have having
here into its itself just more most not now off once only other our out over own same should some such
than that the their them then there these they this those through too under until very was were what
when where which while who whom why will with would you your""".split())


def _top_terms(text, n=40):
    freq = {}
    for w in re.findall(r"[a-zA-Z]{4,}", text.lower()):
        if w not in _STOP:
            freq[w] = freq.get(w, 0) + 1
    return {w for w, _ in sorted(freq.items(), key=lambda kv: -kv[1])[:n]}


def _related_documents(name, terms, top=3):
    """Other uploaded documents that share the most vocabulary with this one."""
    mine = terms[name]
    scored = []
    for other, theirs in terms.items():
        if other == name:
            continue
        shared = mine & theirs
        if shared:
            scored.append((len(shared) / max(1, len(mine | theirs)), other, sorted(shared)[:6]))
    scored.sort(key=lambda x: -x[0])
    return scored[:top]


def _generate(name, text):
    """Ask the LLM for key points and related topics. Returns (result, error)."""
    if call_groq_llm is None:
        return None, "Could not import the LLM helpers: " + _LLM_ERR
    key = get_secret("GROQ_API_KEY")
    if not key:
        return None, "GROQ_API_KEY is not set in Streamlit Secrets."

    context = build_context("main findings contributions conclusions", {name: text}, budget=9000)
    sys_prompt = "You summarise documents accurately. Never invent facts, citations or links."
    user_prompt = (
        f"DOCUMENT:\n{context}\n\n"
        "Reply in exactly this format and nothing else:\n"
        "KEY POINTS:\n"
        "- 5 to 7 short bullets with the most important facts, findings or claims from the document\n"
        "RELATED TOPICS:\n"
        "- 4 to 5 topics or search terms worth reading next (no links)"
    )
    out = call_groq_llm(key, sys_prompt, user_prompt)
    if out.startswith("⚠️"):
        return None, out

    parts = re.split(r"RELATED TOPICS:?", out, flags=re.I)
    key_points = re.sub(r"^\s*KEY POINTS:?", "", parts[0], flags=re.I).strip()
    topics = parts[1].strip() if len(parts) > 1 else ""
    return {
        "key_points": key_points,
        "topics": topics,
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }, ""


def memory_page():
    init_knowledge_base_state()

    st.title("🧠 Memory")
    st.caption("Documents loaded, their key points and related resources.")

    docs = st.session_state.get("documents_list", [])
    raw = st.session_state.get("raw_document_texts", {})
    memory = st.session_state.setdefault("doc_memory", {})
    history = st.session_state.get("query_history", [])

    loaded = [d for d in docs if d.get("name") in raw]
    sample_count = len(docs) - len(loaded)

    m1, m2, m3 = st.columns(3)
    m1.metric("Documents in memory", len(loaded))
    m2.metric("With key points", sum(1 for d in loaded if d["name"] in memory))
    m3.metric("Questions asked", len(history))

    err = st.session_state.pop("mem_error", None)
    if err:
        st.error(err)

    if not loaded:
        st.info("No documents in memory yet. Upload and index a document on the Upload page.")
        if sample_count:
            st.caption(f"{sample_count} sample document(s) have no readable text, so they are not stored here.")
        return

    if st.button("✨ Generate key points for all documents", key="mem_gen_all", type="primary"):
        with st.spinner("Reading documents..."):
            for d in loaded:
                name = d["name"]
                if name in memory:
                    continue
                result, error = _generate(name, raw[name])
                if result:
                    memory[name] = result
                else:
                    st.session_state["mem_error"] = f"{name}: {error}"
                    break
        st.rerun()

    st.markdown("---")
    terms = {n: _top_terms(t) for n, t in raw.items()}

    for i, d in enumerate(loaded):
        name = d["name"]
        entry = memory.get(name)
        with st.expander(f"{'✅' if entry else '⏳'} {name}", expanded=False):
            st.caption(
                f"{d.get('authorityTier', '')} • {d.get('department', '')} • {d.get('size', '')} • "
                f"~{d.get('chunks', 0)} chunks • Loaded {d.get('updated', '')}"
            )

            st.markdown("**Key points**")
            if entry:
                st.markdown(entry["key_points"])
                st.caption(f"Generated {entry['generated']}")
                if st.button("🔄 Regenerate", key=f"mem_regen_{i}"):
                    with st.spinner("Reading document..."):
                        result, error = _generate(name, raw[name])
                    if result:
                        memory[name] = result
                    else:
                        st.session_state["mem_error"] = f"{name}: {error}"
                    st.rerun()
            else:
                st.caption("Not generated yet.")
                if st.button("✨ Generate key points", key=f"mem_gen_{i}"):
                    with st.spinner("Reading document..."):
                        result, error = _generate(name, raw[name])
                    if result:
                        memory[name] = result
                    else:
                        st.session_state["mem_error"] = f"{name}: {error}"
                    st.rerun()

            st.markdown("**Related resources**")
            related = _related_documents(name, terms)
            if related:
                st.markdown("Related uploaded documents:")
                for _, other, shared in related:
                    st.markdown(f"- 📄 **{other}**: shared topics: {', '.join(shared)}")
            else:
                st.caption("No related uploaded documents yet.")

            if entry and entry.get("topics"):
                st.markdown("Suggested topics to read next:")
                st.markdown(entry["topics"])

            asked = [h for h in history if name in h.get("files", [])]
            if asked:
                st.markdown("Questions you asked about this document:")
                for h in asked[:5]:
                    st.markdown(f"- {h['query']}")