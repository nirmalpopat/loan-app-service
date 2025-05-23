from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.domain.models import (
    LoanApplicationCreate,
    LoanApplicationInDB,
    ApplicationStatus
)
from app.usecases.application_handlers import LoanApplicationService
from app.infrastructure.messaging.kafka_client import kafka_client
from app.core.config import settings

router = APIRouter()

@router.post(
    "/",
    response_model=LoanApplicationInDB,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a new loan application",
    description="Submits a new loan application for processing"
)
async def create_application(
    application: LoanApplicationCreate
) -> LoanApplicationInDB:
    """
    Submit a new loan application.
    
    The application will be sent to Kafka for asynchronous processing.
    """
    # Create the application
    db_application = await LoanApplicationService.create_application(application)
    
    # Publish to Kafka for processing
    try:
        await kafka_client.send_message(
            topic=settings.KAFKA_APPLICATION_TOPIC,
            value=application.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit application: {str(e)}"
        )
    
    return db_application

@router.get(
    "/{applicant_id}",
    response_model=LoanApplicationInDB,
    summary="Get application status",
    description="Retrieves the status of the most recent application for the given applicant ID"
)
async def get_application_status(
    applicant_id: str
) -> LoanApplicationInDB:
    """
    Get the status of the most recent loan application for an applicant.
    """
    # Try to get from cache/database
    app_status = await LoanApplicationService.get_application_status(applicant_id)
    
    if not app_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No application found for this applicant ID"
        )
    
    return app_status
