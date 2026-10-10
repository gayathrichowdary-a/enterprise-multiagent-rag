import re
import math
import datetime
from collections import Counter

import pandas as pd
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


def _words(text):
    return re.findall(r"[a-zA-Z]{3,}", text.lower())


def _content_words(text):
    return [w for w in _words(text) if w not in _STOP]


def _cosine(c1, c2):
    dot = sum(c1[w] * c2[w] for w in c1 if w in c2)
    n1 = math.sqrt(sum(v * v for v in c1.values()))
    n2 = math.sqrt(sum(v * v for v in c2.values()))
    return dot / (n1 * n2) if n1 and n2 else 0.0


def _jaccard(s1, s2):
    union = s1 | s2
    return len(s1 & s2) / len(union) if union else 0.0


def _shingles(tokens, n=5):
    return {" ".join(tokens[i:i + n]) for i in range(max(0, len(tokens) - n + 1))}


def compute_metrics(text_a, text_b):
    ca, cb = Counter(_content_words(text_a)), Counter(_content_words(text_b))
    topic = _cosine(ca, cb)
    vocab = _jaccard(set(ca), set(cb))

    sa, sb = _shingles(_words(text_a)), _shingles(_words(text_b))
    copied = len(sa & sb) / min(len(sa), len(sb)) if sa and sb else 0.0

    shared = sorted(((w, ca[w], cb[w]) for w in set(ca) & set(cb)),
                    key=lambda x: -min(x[1], x[2]))[:12]
    only_a = [w for w, _ in ca.most_common(200) if w not in cb][:12]
    only_b = [w for w, _ in cb.most_common(200) if w not in ca][:12]
    return {"topic": topic, "vocab": vocab, "copied": copied,
            "shared": shared, "only_a": only_a, "only_b": only_b}


def _label(topic):
    if topic >= 0.70:
        return "🟢 Very similar content"
    if topic >= 0.40:
        return "🔵 Related topics"
    if topic >= 0.15:
        return "🟡 Slightly related"
    return "🔴 Mostly different topics"


def _ai_compare(name_a, text_a, name_b, text_b):
    if call_groq_llm is None:
        return None, "Could not import the LLM helpers: " + _LLM_ERR
    key = get_secret("GROQ_API_KEY")
    if not key:
        return None, "GROQ_API_KEY is not set in Streamlit Secrets."

    q = "main topics findings claims conclusions"
    ctx_a = build_context(q, {name_a: text_a}, budget=4500)
    ctx_b = build_context(q, {name_b: text_b}, budget=4500)

    sys_prompt = "You compare documents accurately. Use only the text provided. Never invent facts."
    user_prompt = (
        f"DOCUMENT A:\n{ctx_a}\n\nDOCUMENT B:\n{ctx_b}\n\n"
        "Compare the two documents. Use exactly these markdown headings and nothing else:\n"
        "### Summary of Document A\n(2-3 bullets)\n"
        "### Summary of Document B\n(2-3 bullets)\n"
        "### Similarities\n(3-5 bullets)\n"
        "### Differences\n(3-5 bullets)\n"
        "### Conflicts\n(statements where they contradict each other, saying which document says what; "
        "write 'None found' if there are none)\n"
        "### Verdict\n(one sentence on how related they are)"
    )
    out = call_groq_llm(key, sys_prompt, user_prompt)
    if out.startswith("⚠️"):
        return None, out
    return {"text": out, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}, ""


def comparison_page():
    init_knowledge_base_state()

    st.title("⚖️ Compare Documents")
    st.caption("Pick two of your uploaded documents to see how similar they are and where they differ.")

    raw = st.session_state.get("raw_document_texts", {})
    docs = st.session_state.get("documents_list", [])
    meta = {d.get("name"): d for d in docs}
    names = [d["name"] for d in docs if d.get("name") in raw]

    if len(names) < 2:
        st.info(
            f"You need at least 2 documents with readable text. Right now there are {len(names)}. "
            "Go to **Upload Documents**, upload your files and click **Index Staged Files Now**."
        )
        if len(docs) > len(names):
            st.caption("Sample documents have no text, so they cannot be compared.")
        return

    c1, c2 = st.columns(2)
    with c1:
        name_a = st.selectbox("📄 Document A", names, index=0, key="cmp_doc_a")
    with c2:
        name_b = st.selectbox("📄 Document B", names, index=1, key="cmp_doc_b")

    if name_a == name_b:
        st.warning("Choose two different documents.")
        return

    text_a, text_b = raw[name_a], raw[name_b]
    m = compute_metrics(text_a, text_b)

    st.markdown("---")
    st.subheader("📊 How similar are they?")
    st.markdown(f"**{_label(m['topic'])}**")

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Topic similarity", f"{m['topic'] * 100:.1f}%")
        st.progress(min(1.0, m["topic"]))
        st.caption("How much the two use the same important words, weighted by how often.")
    with k2:
        st.metric("Vocabulary overlap", f"{m['vocab'] * 100:.1f}%")
        st.progress(min(1.0, m["vocab"]))
        st.caption("Share of all distinct words that appear in both.")
    with k3:
        st.metric("Copied-text overlap", f"{m['copied'] * 100:.1f}%")
        st.progress(min(1.0, m["copied"]))
        st.caption("Share of identical 5-word sequences. High means shared or copied passages.")

    st.markdown("#### 📋 The two documents")
    rows = []
    for label, n, t in (("A", name_a, text_a), ("B", name_b, text_b)):
        d = meta.get(n, {})
        rows.append({
            "": label,
            "Document": n,
            "Authority tier": d.get("authorityTier", "-"),
            "Reliability": f"{d.get('reliabilityScore', '-')}%",
            "Words": f"{len(_words(t)):,}",
            "Uploaded": d.get("updated", "-"),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🔑 Keywords")
    if m["shared"]:
        st.markdown("**Most important shared words** (times each appears)")
        df = pd.DataFrame(
            {"Document A": [a for _, a, _ in m["shared"]], "Document B": [b for _, _, b in m["shared"]]},
            index=[w for w, _, _ in m["shared"]],
        )
        st.bar_chart(df)
    else:
        st.info("These documents share no important words.")

    u1, u2 = st.columns(2)
    with u1:
        st.markdown("**Only in Document A**")
        st.write(", ".join(m["only_a"]) or "None")
    with u2:
        st.markdown("**Only in Document B**")
        st.write(", ".join(m["only_b"]) or "None")

    st.markdown("---")
    st.subheader("🤖 AI comparison")
    cache = st.session_state.setdefault("doc_compare", {})
    ckey = f"{name_a}||{name_b}"

    if st.button("✨ Generate AI comparison", key="cmp_ai_btn", type="primary"):
        with st.spinner("Reading both documents..."):
            result, error = _ai_compare(name_a, text_a, name_b, text_b)
        if result:
            cache[ckey] = result
        else:
            st.error(error)

    if ckey in cache:
        st.markdown(cache[ckey]["text"])
        st.caption(f"Generated {cache[ckey]['time']}")

    ra = meta.get(name_a, {}).get("reliabilityScore")
    rb = meta.get(name_b, {}).get("reliabilityScore")
    if isinstance(ra, (int, float)) and isinstance(rb, (int, float)):
        st.markdown("---")
        st.subheader("🏛️ If they disagree, which one wins?")
        if ra > rb:
            st.success(f"**{name_a}** takes precedence (reliability {ra}% vs {rb}%).")
        elif rb > ra:
            st.success(f"**{name_b}** takes precedence (reliability {rb}% vs {ra}%).")
        else:
            st.info("Both have the same reliability, so neither takes precedence. Check the dates.")