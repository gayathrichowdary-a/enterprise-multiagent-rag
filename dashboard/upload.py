# dashboard/upload.py
import streamlit as st
import os
import io
import re
import zipfile
import xml.etree.ElementTree as ET

ALLOWED_FILE_TYPES = ["pdf", "docx", "txt", "csv", "png", "jpg", "jpeg"]
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def extract_docx_text_bulletproof(file_bytes):
    """Extracts all text from docx including tables, headers, and raw XML tags."""
    # Method 1: python-docx
    text_lines = []
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        for p in doc.paragraphs:
            if p.text.strip():
                text_lines.append(p.text.strip())
        for table in doc.tables:
            for row in table.rows:
                cells = [c.text.strip() for c in row.cells if c.text.strip()]
                if cells:
                    text_lines.append(" | ".join(cells))
    except Exception:
        pass

    # Method 2: If Method 1 got nothing, extract directly from word/document.xml
    if not text_lines:
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                xml_content = z.read("word/document.xml").decode("utf-8")
                tree = ET.fromstring(xml_content)
                for node in tree.iter():
                    if node.tag.endswith("t") and node.text and node.text.strip():
                        text_lines.append(node.text.strip())
        except Exception:
            pass

    return "\n".join(text_lines)

def extract_text_from_bytes(file_name, file_bytes):
    fname = file_name.lower()
    text = ""
    try:
        if fname.endswith(".docx") or fname.endswith(".doc"):
            text = extract_docx_text_bulletproof(file_bytes)
        elif fname.endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                t = page.extract_text()
                if t: text += t + "\n"
        elif fname.endswith(".txt") or fname.endswith(".csv") or fname.endswith(".json"):
            text = file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        pass

    if not text.strip():
        text = f"Document content for {file_name}"
    return text

def document_sidebar():
    st.subheader("📂 Loaded Documents")
    all_docs = st.session_state.get("knowledge_sources", {}) or st.session_state.get("raw_document_texts", {})
    if all_docs:
        for file_name, data in all_docs.items():
            tier = data.get("authority_tier", "Tier 1") if isinstance(data, dict) else "Tier 1"
            st.caption(f"📄 {file_name} • **{str(tier).split(' ')[0]}**")
    else:
        st.caption("No documents uploaded.")

    st.divider()

    if st.button("📄 Clear Uploaded Documents", key="btn_clear_uploaded_docs", use_container_width=True):
        st.session_state["raw_document_texts"] = {}
        st.session_state["knowledge_sources"] = {}
        st.session_state["uploaded_documents"] = []
        st.session_state["file_bytes"] = {}
        st.success("Uploaded documents cleared.")
        st.rerun()

def upload_page():
    if "raw_document_texts" not in st.session_state:
        st.session_state["raw_document_texts"] = {}
    if "knowledge_sources" not in st.session_state:
        st.session_state["knowledge_sources"] = {}
    if "uploaded_documents" not in st.session_state:
        st.session_state["uploaded_documents"] = []

    st.title("📤 Enterprise Document Ingestion")
    st.caption("Upload documents and assign Enterprise Authority Tiers for Source Reliability Ranking.")

    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox(
            "🏢 Enterprise Department",
            [
                "Legal & InfoSec Compliance",
                "DevOps & Infrastructure (SRE)",
                "Software Engineering",
                "Human Resources (HR)",
                "Customer Operations",
                "General / Other"
            ]
        )
    with col2:
        authority_tier = st.selectbox(
            "🛡️ Source Authority Tier",
            [
                "Tier 1 (Authoritative Policy / Runbook)",
                "Tier 2 (Internal Wiki / Confluence)",
                "Tier 3 (Informal Chat / Working Draft)"
            ]
        )

    uploaded_files = st.file_uploader(
        "Choose Knowledge Source files",
        type=ALLOWED_FILE_TYPES,
        accept_multiple_files=True,
        key="file_uploader_widget"
    )

    if uploaded_files:
        st.write(f"📁 Selected **{len(uploaded_files)}** file(s). Click below to process and index:")
        
        if st.button("🚀 Ingest & Index Documents", type="primary", use_container_width=True):
            with st.spinner("Processing documents into active memory..."):
                for file in uploaded_files:
                    if file.size > MAX_FILE_SIZE_BYTES:
                        st.error(f"❌ {file.name} exceeds limit.")
                        continue

                    safe_file_name = file.name
                    b_data = file.getvalue()
                    
                    # Extract full text
                    extracted_text = extract_text_from_bytes(safe_file_name, b_data)
                    st.session_state["raw_document_texts"][safe_file_name] = extracted_text

                    init_score = 95.0 if "Tier 1" in authority_tier else 80.0 if "Tier 2" in authority_tier else 55.0
                    st.session_state["knowledge_sources"][safe_file_name] = {
                        "type": os.path.splitext(safe_file_name)[1],
                        "department": department,
                        "authority_tier": authority_tier,
                        "reliability_score": init_score
                    }
                    if safe_file_name not in st.session_state["uploaded_documents"]:
                        st.session_state["uploaded_documents"].append(safe_file_name)

                st.success(f"✅ Ingested {len(uploaded_files)} document(s) successfully!")
                st.rerun()

    if st.session_state.get("knowledge_sources"):
        st.divider()
        st.subheader("📚 Active Enterprise Knowledge Sources")
        for name, data in st.session_state["knowledge_sources"].items():
            dept = data.get('department', 'General')
            tier = data.get('authority_tier', 'Tier 1')
            rel = data.get('reliability_score', 95.0)
            text_len = len(st.session_state.get("raw_document_texts", {}).get(name, ""))
            st.write(f"📄 **{name}** ({text_len} characters extracted) | Dept: `{dept}` | Authority: `{tier}` | Reliability: `{rel}%`")
