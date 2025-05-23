import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(command, cwd=None):
    print(f"Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return process

def main():
    # Set environment variables
    os.environ.update({
        "APP_ENV": "development",
        "DEBUG": "True",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "postgres",
        "POSTGRES_DB": "loan_app",
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
        "KAFKA_APPLICATION_TOPIC": "loan_applications",
        "KAFKA_CONSUMER_GROUP_ID": "loan_processor"
    })

    # Start Redis
    redis_process = run_command("redis-server --port 6379")
    
    # Start Zookeeper (simplified for local development)
    zookeeper_process = run_command("bin/zookeeper-server-start.sh config/zookeeper.properties")
    
    # Start Kafka (simplified for local development)
    kafka_process = run_command("bin/kafka-server-start.sh config/server.properties")
    
    # Wait for services to start
    time.sleep(10)
    
    try:
        # Start the Kafka consumer in the background
        consumer_process = run_command("python -m scripts.kafka_consumer")
        
        # Start the FastAPI application
        fastapi_process = run_command("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        
        # Wait for the FastAPI process to complete
        fastapi_process.wait()
        
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Clean up processes
        for process in [fastapi_process, consumer_process, kafka_process, zookeeper_process, redis_process]:
            if 'process' in locals() and process.poll() is None:
                process.terminate()
                process.wait()

if __name__ == "__main__":
    main()
