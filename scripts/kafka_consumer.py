import asyncio
import logging
from typing import Dict, Any
from app.core.config import settings
from app.infrastructure.messaging.kafka_client import kafka_client
from app.usecases.application_handlers import LoanApplicationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def process_application(message: Dict[str, Any]) -> None:
    """Process a loan application message from Kafka"""
    try:
        logger.info(f"Processing application: {message}")
        await LoanApplicationService.process_application(message)
    except Exception as e:
        logger.error(f"Error processing application: {e}", exc_info=True)
        raise

async def main():
    logger.info("Starting Kafka consumer...")
    
    try:
        await kafka_client.start()
        
        logger.info("Kafka consumer started. Waiting for messages...")
        
        await kafka_client.consume_messages(
            topic=settings.KAFKA_APPLICATION_TOPIC,
            group_id=settings.KAFKA_CONSUMER_GROUP_ID,
            process_message=process_application
        )
        
    except asyncio.CancelledError:
        logger.info("Shutting down Kafka consumer...")
    except Exception as e:
        logger.error(f"Error in Kafka consumer: {e}", exc_info=True)
    finally:
        await kafka_client.stop()
        logger.info("Kafka consumer stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
