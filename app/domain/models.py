from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"

class LoanApplicationBase(BaseModel):
    applicant_id: str = Field(..., description="Unique identifier for the applicant")
    amount: float = Field(..., gt=0, description="Loan amount (must be greater than 0)")
    term_months: int = Field(..., ge=1, le=60, description="Loan term in months (1-60)")

class LoanApplicationCreate(LoanApplicationBase):
    pass

class LoanApplicationInDB(LoanApplicationBase):
    id: UUID = Field(default_factory=uuid4)
    status: ApplicationStatus = ApplicationStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class LoanApplicationResponse(LoanApplicationInDB):
    class Config:
        from_attributes = True
