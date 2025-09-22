import os
from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from models import VerificationResponse
from database import get_db, PlotDocument
from services.storage import save_file
from services.ocr import extract_text_from_file
from services.verifier import verify_documents

app = FastAPI(title="Land Document Verification API")

UPLOAD_DIR = "uploads"

@app.post("/submit", response_model=VerificationResponse)
async def submit_documents(
    plot_id: str = Form(...),
    titre_foncier: UploadFile = Form(...),
    quittance: UploadFile = Form(...),
    db: Session = Depends(get_db),
):
    try:
        # Sauvegarde
        saved_title = save_file(titre_foncier, UPLOAD_DIR)
        saved_quittance = save_file(quittance, UPLOAD_DIR)

        # OCR
        text_title = extract_text_from_file(saved_title)
        text_quittance = extract_text_from_file(saved_quittance)

        extracted_docs = {
            "titre_foncier": text_title,
            "quittance": text_quittance
        }

        # Vérification IA
        result = verify_documents(plot_id, extracted_docs, db)

        return VerificationResponse(
            status=result["status"],
            message=result["message"],
            details=result["details"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





