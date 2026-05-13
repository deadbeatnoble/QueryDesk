from fastapi import FastAPI
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from models.document import Document
from utils.llm_service import generate_answer

from services.ingestion_service import ingest_document
from services.retrieve_relevant_chunks import retrieve_relevant_chunks

from fastapi import UploadFile, File
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

class DocumentCreate(BaseModel):
    name: str
    file_type: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/documents")
def get_documents():
    db = SessionLocal()
    documents = db.query(Document).all()

    return documents

@app.delete("/documents/{document_id}")
def delete_document(document_id: int):
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == document_id).first()

    if not doc:
        return {"message": "Document not found"}

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    db = SessionLocal()
    
    return ingest_document(file, db)

@app.post("/ask")
def ask_question(payload: dict):

    db = SessionLocal()

    top_chunks = retrieve_relevant_chunks(
        payload["question"],
        db
    )

    context = "\n\n".join(
        [c["content"] for c in top_chunks]
    )

    answer = generate_answer(
        payload["question"],
        context
    )

    return {
        "answer": answer,
        "source": top_chunks
    }