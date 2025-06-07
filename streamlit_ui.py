import streamlit as st
import requests

BASE_URL = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="📈 Stock Market Agentic Chatbot",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("📈 Stock Market Agentic Chatbot")

# Sidebar: Upload documents
with st.sidebar:
    st.header("📄 Upload Documents")
    st.markdown("Upload **stock market PDFs or DOCX** to create knowledge base.")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("Upload and Ingest"):
        if not uploaded_files:
            st.warning("Please upload files first")
        else:
            files = [("files", (f.name, f.read(), f.type)) for f in uploaded_files]
            with st.spinner("Uploading and processing files..."):
                response = requests.post(f"{BASE_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success("✅ File uplaoded and processed successfully!")
                else:
                    st.error("❌ Upload failed: " + response.text)

# Display chat history
st.header("Ask a Question")
st.markdown("Enter your **stock-market related** question. The chatbot will search will search the documents and respond intelligently.")

question = st.text_input("Your Question", placeholder="e.g. What are the financials of Apple Inc?")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            payload = {"question": question}
            response = requests.post(f"{BASE_URL}/query", json=payload)
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned")
                st.markdown("### Answer")
                st.write(answer)
            else:
                st.error("❌ Failed to get answer: " + response.text)
