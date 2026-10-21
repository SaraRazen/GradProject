from pydantic import BaseModel


class PatientResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool