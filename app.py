import streamlit as st
from pathlib import Path

from enhancer import enhance_resume
from comparator import build_unified_diff

# Reusing PDF/text extraction logic without changing architecture
from resume_reader import ResumeDocument

st.set_page_config(page_title="Resume Enhancer", layout="centered")

def read_uploaded_file(uploaded_file) -> ResumeDocument:
    """
    Convert Streamlit's UploadedFile into the same ResumeDocument shape.
    - If txt: decode bytes
    - If pdf: write to a temp file path and reuse pdfplumber extraction via read_resume() logic
    """
    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix == ".txt":
        raw = uploaded_file.getvalue()
        text = raw.decode("utf-8", errors="replace")
        return ResumeDocument(path=Path(uploaded_file.name), ext=".txt", text=text)

    if suffix == ".pdf":
        # temp file so pdfplumber can open it
        import tempfile
        from resume_reader import read_resume

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = Path(tmp.name)

        return read_resume(tmp_path)

    raise ValueError("Only .txt or .pdf supported")


st.set_page_config(page_title="InfinityBit Resume Enhancer", layout="centered")

st.title("AI-Powered Resume Enhancer")
st.caption("Upload a resume (.pdf / .txt), choose a target role, get an enhanced version + a diff.")

uploaded = st.file_uploader("Upload your resume", type=["pdf", "txt"])
role = st.text_input("Target role (e.g., Backend Developer, Data Analyst)")

run = st.button("Enhance Resume", type="primary", disabled=(uploaded is None or not role.strip()))

if run:
    with st.spinner("Reading resume..."):
        doc = read_uploaded_file(uploaded)

    with st.spinner("Calling LLM (Groq)..."):
        enhanced = enhance_resume(doc.text, target_role=role.strip())

    diff_result = build_unified_diff(
        original_text=doc.text,
        enhanced_text=enhanced,
        from_name=f"{Path(uploaded.name).stem}_original",
        to_name=f"{Path(uploaded.name).stem}_enhanced",
    )

    st.success("Done!")

    st.subheader("Preview (Enhanced)")
    st.text_area("Enhanced resume (preview)", enhanced, height=250)

    st.subheader("Diff summary")
    st.write(f"Changed lines: {diff_result.changed_lines}")

    st.download_button(
        "Download enhanced resume",
        data=enhanced.encode("utf-8"),
        file_name=f"enhanced_{Path(uploaded.name).stem}.txt",
        mime="text/plain",
    )

    st.download_button(
        "Download changes diff",
        data=diff_result.diff_text.encode("utf-8"),
        file_name=f"diff_{Path(uploaded.name).stem}.txt",
        mime="text/plain",
    )