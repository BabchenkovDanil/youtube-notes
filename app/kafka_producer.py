from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = None


def get_producer():
    global producer
    if producer is not None:
        return producer

    logger.info("Connecting to Kafka...")
    for attempt in range(10):
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Kafka producer connected")
            return producer
        except NoBrokersAvailable:
            logger.warning(f"Kafka not ready, attempt {attempt + 1}/10, waiting 2 seconds...")
            time.sleep(2)

    raise Exception("Could not connect to Kafka after 10 attempts")


def send_video_task(video_id: str, owner_id: int):
    message = {
        'video_id': video_id,
        'owner_id': owner_id
    }
    print(f"Sending to Kafka: {message}")
    prod = get_producer()
    prod.send('video-events', value=message)
    prod.flush()

