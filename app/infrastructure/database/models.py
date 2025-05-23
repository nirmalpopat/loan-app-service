from sqlalchemy import Column, String, Float, Integer, DateTime, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid
from datetime import datetime

from app.domain.models import ApplicationStatus
from .base import Base

class LoanApplicationDB(Base):
    __tablename__ = "loan_applications"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    applicant_id = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    status = Column(SQLEnum(ApplicationStatus), nullable=False, default=ApplicationStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    def to_domain(self):
        from app.domain.models import LoanApplicationInDB
        return LoanApplicationInDB(
            id=self.id,
            applicant_id=self.applicant_id,
            amount=self.amount,
            term_months=self.term_months,
            status=self.status,
            created_at=self.created_at,
            processed_at=self.processed_at
        )
