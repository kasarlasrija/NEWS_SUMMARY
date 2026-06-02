import streamlit as st
import PyPDF2
import docx
from fpdf import FPDF
from datetime import datetime

st.set_page_config(
    page_title="AI Meeting Minutes Summarizer",
    page_icon="🤖",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

if "notes" not in st.session_state:
    st.session_state.notes = ""

def generate_summary(text):
    sentences = text.replace("\n", " ").split(".")
    sentences = [s.strip() for s in sentences if s.strip()]
    return ". ".join(sentences[:3])

def read_pdf(uploaded_file):
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    except Exception:
        pass

    return text

def read_docx(uploaded_file):
    text = ""

    try:
        document = docx.Document(uploaded_file)

        for para in document.paragraphs:
            text += para.text + "\n"

    except Exception:
        pass

    return text

def create_pdf(summary):
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(
        0,
        10,
        summary
    )

    file_name = "meeting_summary.pdf"

    pdf.output(file_name)

    return file_name

st.sidebar.title("🤖 AI Summarizer")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Summarizer",
        "History",
        "Model Info",
        "About"
    ]
)

if menu == "Home":

    st.title("🤖 AI Meeting Minutes Summarizer")

    st.markdown("""
    ### Welcome

    This application automatically generates concise summaries from long meeting notes.

    ### Features

    ✅ Meeting Notes Summarization

    ✅ PDF Upload

    ✅ DOCX Upload

    ✅ Download Summary as PDF

    ✅ Download Summary as TXT

    ✅ Summary Statistics

    ✅ Streamlit Deployment Ready
    """)

elif menu == "Summarizer":

    st.title("📝 AI Meeting Minutes Summarizer")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Load Example"):

            st.session_state.notes = """
            Yesterday the development team completed authentication APIs.

            Frontend integration was completed.

            Testing begins next Monday.

            Sprint review meeting scheduled Friday.

            Client demo planned next week.
            """

    with col2:

        if st.button("Clear Notes"):

            st.session_state.notes = ""

    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"]
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".pdf"):

            st.session_state.notes = read_pdf(
                uploaded_file
            )

        elif uploaded_file.name.endswith(".docx"):

            st.session_state.notes = read_docx(
                uploaded_file
            )

        st.success("File uploaded successfully.")

    meeting_notes = st.text_area(
        "Enter Meeting Notes",
        value=st.session_state.notes,
        height=300
    )

    if st.button("🚀 Generate Summary"):

        if meeting_notes.strip() == "":

            st.warning(
                "Please enter meeting notes."
            )

        else:

            summary = generate_summary(
                meeting_notes
            )

            st.subheader(
                "AI Generated Summary"
            )

            st.success(summary)

            original_words = len(
                meeting_notes.split()
            )

            summary_words = len(
                summary.split()
            )

            compression_ratio = round(
                (
                    (original_words - summary_words)
                    / original_words
                ) * 100,
                2
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Original Words",
                original_words
            )

            c2.metric(
                "Summary Words",
                summary_words
            )

            c3.metric(
                "Compression %",
                f"{compression_ratio}%"
            )

            st.session_state.history.append(
                {
                    "timestamp": str(datetime.now()),
                    "summary": summary
                }
            )

            pdf_file = create_pdf(summary)

            with open(pdf_file, "rb") as f:

                st.download_button(
                    "📄 Download Summary as PDF",
                    data=f,
                    file_name="meeting_summary.pdf",
                    mime="application/pdf"
                )

            st.download_button(
                "📃 Download Summary as TXT",
                data=summary,
                file_name="meeting_summary.txt"
            )

elif menu == "History":

    st.title("📚 Summary History")

    if len(st.session_state.history) == 0:

        st.info(
            "No summaries generated yet."
        )

    else:

        for item in reversed(
            st.session_state.history
        ):

            st.write(
                f"🕒 {item['timestamp']}"
            )

            st.success(
                item["summary"]
            )

elif menu == "Model Info":

    st.title("🧠 Model Information")

    st.markdown("""
    ### Encoder

    - Embedding Layer
    - LSTM Encoder
    - Context Vector

    ### Decoder

    - Embedding Layer
    - LSTM Decoder
    - Dense Layer
    - Summary Generation

    ### Training

    Article

    ↓

    Encoder

    ↓

    Context Vector

    ↓

    Decoder

    ↓

    Summary
    """)

elif menu == "About":

    st.title("ℹ About Project")

    st.write(
        "AI Meeting Minutes Summarizer using Seq2Seq Encoder-Decoder Architecture."
    )

    st.write(
        "Developed using Python, TensorFlow and Streamlit."
    )

    st.write(
        "Supports meeting notes entered manually or uploaded as PDF/DOCX files."
    )