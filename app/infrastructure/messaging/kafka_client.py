from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import asyncio
from typing import Dict, Any, Optional, Callable, Awaitable
from app.core.config import settings

class KafkaClient:
    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumer: Optional[AIOKafkaConsumer] = None
    
    async def start(self):
        """Start the Kafka producer"""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            security_protocol="PLAINTEXT"
        )
        await self.producer.start()
    
    async def stop(self):
        """Stop the Kafka producer and consumer"""
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()
    
    async def send_message(self, topic: str, value: Dict[str, Any], key: Optional[bytes] = None):
        """Send a message to a Kafka topic"""
        if not self.producer:
            raise RuntimeError("Producer not started. Call start() first.")
        
        try:
            await self.producer.send_and_wait(topic=topic, value=value, key=key)
        except Exception as e:
            print(f"Error sending message to Kafka: {e}")
            raise
    
    async def consume_messages(
        self,
        topic: str,
        group_id: str,
        process_message: Callable[[Dict[str, Any]], Awaitable[None]]
    ) -> None:
        """Consume messages from a Kafka topic"""
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=group_id,
            auto_offset_reset=settings.KAFKA_AUTO_OFFSET_RESET,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            security_protocol="PLAINTEXT"
        )
        
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    await process_message(msg.value)
                except Exception as e:
                    print(f"Error processing message: {e}")
        finally:
            await self.stop()

kafka_client = KafkaClient()
