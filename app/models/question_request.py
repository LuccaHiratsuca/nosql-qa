from typing import Optional
from pydantic import BaseModel

# ----------------------------------------------------------------------
#            MODELO DE REQUISIÇÃO /ask
# ----------------------------------------------------------------------

class QuestionRequest(BaseModel):
    user_id: str
    excel_id: Optional[str] = None
    question: str