"""CV/Resume text extraction and research interest summarization."""
import fitz  # PyMuPDF
from docx import Document
from io import BytesIO
from anthropic import Anthropic
import os

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX bytes."""
    doc = Document(BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract text based on file extension."""
    filename_lower = filename.lower()
    if filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {filename}")


def summarize_research_interests(cv_text: str) -> str:
    """Use Claude to extract and summarize research interests from CV text."""
    # Truncate if too long (Claude context limits)
    max_chars = 15000
    if len(cv_text) > max_chars:
        cv_text = cv_text[:max_chars]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this CV/resume and extract the person's research interests,
technical skills, and academic focus areas. Summarize in 2-3 concise paragraphs
that would help match them with potential research advisors.

Focus on:
- Research topics and methodologies
- Technical domains and tools
- Academic interests and thesis/project themes

CV Text:
{cv_text}

Research Interest Summary:"""
            }
        ]
    )
    return response.content[0].text
