import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from database import PlotDocument

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ai_semantic_check_gemini(extracted_docs: dict, reference_docs: dict) -> dict:
    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = f"""
    Tu es un expert en analyse et détection de fraudes dans les documents fonciers.
    
    Documents de référence (base officielle) :
    {reference_docs}

    Documents soumis (OCR JSON page par page) :
    {extracted_docs}

    Tâches :
    1. Vérifie la conformité avec les informations officielles.
    2. Vérifie l’authenticité : détection falsification, incohérences, pages modifiées.
    3. Détecte les fraudes possibles (doublons, noms contradictoires, parcelle déjà vendue).
    4. Vérifie la présence et la cohérence des signatures, tampons ou mentions légales.
    5. Retourne uniquement un JSON au format :
    {{
      "status": "APPROVED" | "REJECTED",
      "reason": "explication claire",
      "anomalies": [liste d’anomalies détectées si REJECTED]
    }}
    """

    response = model.generate_content(prompt)
    try:
        return eval(response.text)
    except Exception:
        return {"status": "REJECTED", "reason": "Erreur d'analyse IA", "anomalies": []}

def verify_documents(plot_id: str, extracted_docs: dict, db: Session):
    docs = db.query(PlotDocument).filter(PlotDocument.plot_id == plot_id).all()
    if not docs:
        return {
            "status": "REJECTED",
            "message": "Aucun document officiel trouvé pour cette parcelle.",
            "details": {"plot_id": plot_id}
        }

    reference_docs = {doc.document_type: doc.document_name for doc in docs}
    result = ai_semantic_check_gemini(extracted_docs, reference_docs)

    if result["status"] == "APPROVED":
        return {"status": "APPROVED", "message": "Documents conformes.", "details": result}
    else:
        return {"status": "REJECTED", "message": "Incohérence détectée.", "details": result}
