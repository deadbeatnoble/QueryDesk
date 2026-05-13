from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from database import SessionLocal
from models.document import Document
from models.chunk import DocumentChunk
from utils.chunking import chunk_text
from utils.embedding import get_embeddings

async def ingest_document(file: UploadFile = File(...)):
    upload_path = f"uploads/{file.filename}"

    with open(upload_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    ext = file.filename.split(".")[-1].lower()

    extracted_text = ""

    if ext == "pdf":
        reader = PdfReader(upload_path)

        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"

    db = SessionLocal()
    doc = Document(name = file.filename, file_type = ext)

    db.add(doc)
    db.commit()
    db.refresh(doc)

    chunks = chunk_text(extracted_text)

    for index, chunk in enumerate(chunks):
        vector = get_embeddings(chunk)

        db_chunk = DocumentChunk(
            document_id = doc.id,
            chunk_index = index,
            content = chunk,
            embedding = str(vector) #temporary solution
        )

        db.add(db_chunk)

    db.commit()

    return {
        "message": "uploaded",
        "filename": doc.name,
        "characters_extracted": len(extracted_text)
    }