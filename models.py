from pydantic import BaseModel
from typing import Optional, Dict

class VerificationResponse(BaseModel):
    status: str   # APPROVED | REJECTED
    message: str
    details: Optional[Dict] = None
