# src/generator.py
import os
import random
from datetime import datetime, timedelta
from faker import Faker
from docx import Document
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
import io

fake = Faker()

CUSTODIANS = [
    {"name": "Sarah Jenkins", "email": "sjenkins@apexcorp.com", "role": "VP of Operations"},
    {"name": "David Ross", "email": "dross@apexcorp.com", "role": "Procurement Director"},
    {"name": "Elena Rostova", "email": "erostova@nexustech.io", "role": "Vendor Lead"},
    {"name": "Michael Chang", "email": "mchang@apexcorp.com", "role": "Legal Counsel"}
]

TOPICS = [
    "Q3 Vendor Performance Review",
    "Notice of Breach - Section 4.2 Delay",
    "Contract Termination Notice",
    "SLA Penalties Discussion",
    "Weekly Sync Minutes"
]

def generate_pdf_bytes(text: str) -> bytes:
    """Helper to generate a basic PDF in-memory."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    y = 800
    for line in text.split('\n'):
        c.drawString(50, y, line[:90])
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def generate_docx_bytes(text: str) -> bytes:
    """Helper to generate a Word doc in-memory."""
    doc = Document()
    doc.add_paragraph(text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def create_synthetic_corpus(output_dir: str = "data/raw", count: int = 100):
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    
    for i in range(1, count + 1):
        doc_id = f"DOC_{i:04d}"
        sender = random.choice(CUSTODIANS)
        recipient = random.choice([c for c in CUSTODIANS if c != sender])
        topic = random.choice(TOPICS)
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        
        body = (
            f"DATE: {date}\n"
            f"FROM: {sender['name']} <{sender['email']}>\n"
            f"TO: {recipient['name']} <{recipient['email']}>\n"
            f"SUBJECT: {topic}\n\n"
            f"Dear {recipient['name']},\n\n"
            f"{fake.paragraph(nb_sentences=5)}\n\n"
            f"Regarding the matter of {topic.lower()}, we need to assess our legal standing.\n"
            f"{fake.paragraph(nb_sentences=3)}\n\n"
            f"Best regards,\n{sender['name']}"
        )
        
        # Randomly choose file format
        file_type = random.choice(["pdf", "docx", "txt"])
        filename = f"{doc_id}_{sender['name'].replace(' ', '_')}.{file_type}"
        filepath = os.path.join(output_dir, filename)
        
        if file_type == "txt":
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(body)
        elif file_type == "pdf":
            with open(filepath, "wb") as f:
                f.write(generate_pdf_bytes(body))
        elif file_type == "docx":
            with open(filepath, "wb") as f:
                f.write(generate_docx_bytes(body))
                
        generated_files.append(filepath)

    # Force Exact Duplicates (simulating eDiscovery duplicate documents)
    for dup_idx in range(5):
        source_file = generated_files[dup_idx]
        file_ext = source_file.split('.')[-1]
        dup_filename = f"DOC_DUP_{dup_idx+1:04d}_COPY.{file_ext}"
        dup_filepath = os.path.join(output_dir, dup_filename)
        with open(source_file, "rb") as src, open(dup_filepath, "wb") as dst:
            dst.write(src.read())

    print(f"✅ Generated {count + 5} synthetic eDiscovery documents in '{output_dir}'.")

if __name__ == "__main__":
    create_synthetic_corpus()