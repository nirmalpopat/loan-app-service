import pytest
from fastapi import status
from app.domain.models import ApplicationStatus

TEST_APPLICATION = {
    "applicant_id": "test_user_123",
    "amount": 5000,
    "term_months": 12
}

@pytest.mark.asyncio
async def test_create_application(test_app, mock_kafka):
    # Mock the Kafka producer
    mock_kafka.send_message.return_value = None
    
    # Send a test application
    response = test_app.post("/api/v1/applications/", json=TEST_APPLICATION)
    
    # Verify the response
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    assert data["applicant_id"] == TEST_APPLICATION["applicant_id"]
    assert data["amount"] == TEST_APPLICATION["amount"]
    assert data["term_months"] == TEST_APPLICATION["term_months"]
    assert data["status"] == ApplicationStatus.PENDING.value
    
    # Verify Kafka was called
    mock_kafka.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_get_application_status(test_app, mock_redis):
    # Mock the Redis response
    test_status = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "applicant_id": "test_user_123",
        "amount": 5000,
        "term_months": 12,
        "status": "approved",
        "created_at": "2023-01-01T00:00:00",
        "processed_at": "2023-01-01T00:01:00"
    }
    mock_redis.get.return_value = test_status
    
    # Request the application status
    response = test_app.get(f"/api/v1/applications/{test_status['applicant_id']}")
    
    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["applicant_id"] == test_status["applicant_id"]
    assert data["status"] == test_status["status"]
    
    # Verify Redis was called with the correct key
    mock_redis.get.assert_called_once_with(f"app_status:{test_status['applicant_id']}")

@pytest.mark.asyncio
async def test_get_nonexistent_application(test_app, mock_redis):
    # Mock Redis to return None (not found)
    mock_redis.get.return_value = None
    
    # Request status for a non-existent application
    response = test_app.get("/api/v1/applications/nonexistent_user")
    
    # Verify the response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "No application found" in response.json()["detail"]
