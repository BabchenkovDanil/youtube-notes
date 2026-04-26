from kafka import KafkaConsumer
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Video
from app.youtube_service import get_video_info

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

consumer = KafkaConsumer(
    'video-events',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print('Consumer started. Waiting for messages...')

for message in consumer:
    print(f"Received message: {message.value}")
    data = message.value
    video_id = data['video_id']
    owner_id = data['owner_id']
    print(f"Processing video: {video_id} for user {owner_id}")

    video_info = get_video_info(video_id)
    if not video_info:
        print(f'Failed to fetch info for {video_id}')
        continue

    db = SessionLocal()

    try:
        existing = db.query(Video).filter(Video.club_id == video_id).first()
        if existing:
            print(f'Video {video_id} already exists')
            continue

        new_video = Video(
            club_id=video_id,
            title=video_info['title'],
            description=video_info['description'],
            thumbnail=video_info['thumbnail'],
            owner_id=owner_id
        )
        db.add(new_video)
        db.commit()
        db.refresh(new_video)
        print(f'Video {video_id} sevad to DB with id {new_video.id}')
    finally:
        db.close()