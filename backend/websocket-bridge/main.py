"""
WebSocket Bridge - Kafka to Socket.io Bridge

Subscribes to Kafka topics and publishes events to Socket.io for real-time frontend updates.
"""

import os
import logging
import json
import asyncio
from typing import Dict, Any
import socketio
from aiohttp import web
from kafka import KafkaConsumer
from threading import Thread

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
SOCKETIO_PORT = int(os.getenv("SOCKETIO_PORT", "4001"))

# Topics to subscribe to
KAFKA_TOPICS = [
    "agent-logs",
    "agent-status",
    "mastery-updates",
    "student-struggle",
    "triage-routing",
    "agent-responses"
]

# Create Socket.io server
sio = socketio.AsyncServer(
    async_mode='aiohttp',
    cors_allowed_origins='*',  # In production, restrict to your frontend URL
    logger=True,
    engineio_logger=True
)

app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    logger.info(f"Client connected: {sid}")
    await sio.emit('connection_status', {'status': 'connected', 'sid': sid}, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")


@sio.event
async def subscribe(sid, data):
    """
    Handle client subscription to specific topics

    Example: {'topics': ['agent-logs', 'mastery-updates']}
    """
    topics = data.get('topics', [])
    logger.info(f"Client {sid} subscribing to topics: {topics}")

    # In Socket.io, we use rooms for topic-based subscriptions
    for topic in topics:
        await sio.enter_room(sid, topic)

    await sio.emit('subscribed', {'topics': topics}, room=sid)


def process_kafka_message(topic: str, message_data: Dict[str, Any]):
    """
    Process Kafka message and determine Socket.io event

    Args:
        topic: Kafka topic name
        message_data: Message data
    """
    try:
        # Extract event type and data
        event_type = message_data.get('event_type', 'unknown')
        service_name = message_data.get('service_name', 'unknown')
        data = message_data.get('data', {})

        # Map Kafka topics to Socket.io events
        if topic == "agent-logs":
            # Emit agent log event
            asyncio.create_task(
                sio.emit('agent-log', {
                    'agent': service_name,
                    'event_type': event_type,
                    'timestamp': message_data.get('timestamp'),
                    'data': data
                })
            )

        elif topic == "agent-status":
            # Emit agent status update
            asyncio.create_task(
                sio.emit('agent-status', {
                    'agent': service_name,
                    'status': data.get('status', 'unknown'),
                    'timestamp': message_data.get('timestamp'),
                    'data': data
                })
            )

        elif topic == "mastery-updates":
            # Emit mastery update event
            asyncio.create_task(
                sio.emit('mastery-update', {
                    'student_id': data.get('student_id'),
                    'topic': data.get('topic'),
                    'old_mastery': data.get('old_mastery', 0.0),
                    'new_mastery': data.get('new_mastery', 0.0),
                    'struggling_topics': data.get('struggling_topics', []),
                    'timestamp': message_data.get('timestamp')
                })
            )

        elif topic == "student-struggle":
            # Emit student struggle alert
            asyncio.create_task(
                sio.emit('student-struggle', {
                    'student_id': data.get('student_id'),
                    'confidence': data.get('confidence', 0.0),
                    'indicators': data.get('indicators', []),
                    'interventions': data.get('interventions', []),
                    'timestamp': message_data.get('timestamp')
                })
            )

        elif topic == "triage-routing":
            # Emit routing decision
            asyncio.create_task(
                sio.emit('routing-decision', {
                    'query_id': data.get('query_id'),
                    'student_id': data.get('student_id'),
                    'detected_intent': data.get('detected_intent'),
                    'routed_to_agent': data.get('routed_to_agent'),
                    'confidence_score': data.get('confidence_score', 0.0),
                    'timestamp': message_data.get('timestamp')
                })
            )

        elif topic == "agent-responses":
            # Emit agent response
            asyncio.create_task(
                sio.emit('agent-response', {
                    'query_id': data.get('query_id'),
                    'student_id': data.get('student_id'),
                    'response': data.get('response'),
                    'timestamp': message_data.get('timestamp')
                })
            )

        logger.debug(f"Processed message from {topic}: {event_type}")

    except Exception as e:
        logger.error(f"Error processing Kafka message from {topic}: {e}", exc_info=True)


def kafka_consumer_thread():
    """
    Kafka consumer thread

    Subscribes to Kafka topics and processes messages.
    """
    logger.info(f"Starting Kafka consumer for topics: {KAFKA_TOPICS}")

    consumer = KafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id='websocket-bridge-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )

    logger.info("Kafka consumer started successfully")

    for message in consumer:
        try:
            process_kafka_message(
                topic=message.topic,
                message_data=message.value
            )
        except Exception as e:
            logger.error(f"Error in Kafka consumer: {e}", exc_info=True)


# Health check endpoint
async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        'status': 'healthy',
        'service': 'websocket-bridge',
        'version': '1.0.0',
        'kafka_topics': KAFKA_TOPICS
    })


# Add routes
app.router.add_get('/health', health_check)


if __name__ == '__main__':
    # Start Kafka consumer in background thread
    kafka_thread = Thread(target=kafka_consumer_thread, daemon=True)
    kafka_thread.start()

    logger.info(f"Starting WebSocket Bridge on port {SOCKETIO_PORT}...")

    # Start Socket.io server
    web.run_app(app, host='0.0.0.0', port=SOCKETIO_PORT)
