from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any
import json

from app.domain.models import (
    LoanApplicationCreate, 
    LoanApplicationInDB,
    ApplicationStatus
)
from app.infrastructure.database.models import LoanApplicationDB
from app.infrastructure.database.base import get_db
from app.infrastructure.cache.redis_client import redis_cache

class LoanApplicationService:
    @staticmethod
    async def create_application(
        application: LoanApplicationCreate
    ) -> LoanApplicationInDB:
        """Create a new loan application"""
        # In a real application, we can validate business rules here
        db_application = LoanApplicationInDB(**application.dict())
        
        # In a real app, we would save to the database here
        # For now, we'll just return the created application
        return db_application
    
    @staticmethod
    async def process_application(application_data: Dict[str, Any]) -> None:
        """Process a loan application from Kafka"""
        try:
            # Validate the application
            application = LoanApplicationCreate(**application_data)
            
            # Simple validation logic
            if application.amount <= 0:
                status = ApplicationStatus.REJECTED
            elif application.amount > 50000:  # Example threshold
                status = ApplicationStatus.REJECTED
            else:
                status = ApplicationStatus.APPROVED
            
            # Create the processed application
            processed_app = LoanApplicationInDB(
                **application.dict(),
                status=status,
                processed_at=datetime.utcnow()
            )
            
            # Convert to dict and ensure datetime and UUID are properly serialized
            app_dict = processed_app.dict()
            app_dict['processed_at'] = app_dict['processed_at'].isoformat() if app_dict['processed_at'] else None
            app_dict['created_at'] = app_dict['created_at'].isoformat()
            app_dict['id'] = str(app_dict['id'])  # Convert UUID to string
            
            # Store in Redis with proper JSON serialization
            await redis_cache.set(
                f"app_status:{processed_app.applicant_id}",
                json.dumps(app_dict)
            )
            
            print(f"Processed application: {processed_app}")
            
        except Exception as e:
            print(f"Error processing application: {e}")
            raise
    
    @staticmethod
    async def get_application_status(
        applicant_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get the status of an application"""
        # Try to get from cache first
        cached_status = await redis_cache.get(f"app_status:{applicant_id}")
        if cached_status:
            return json.loads(cached_status)
        
        # If not in cache, get from database
        # In a real app, we would query the database here
        # For now, return None if not in cache
        return None
