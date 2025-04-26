import pytest
import os
import time
from google.cloud import pubsub_v1
from flask import Flask

PROJECT = "test-project"
TOPICS = {
    "products": "inventarios-products",
    "orders": "inventarios-orders",
    "stock": "inventarios-stock",  
}

SUBS = {
    "inventarios-products": "sub-products",
    "inventarios-orders": "sub-orders",
    "inventarios-stock": "sub-stock",
}

@pytest.fixture(scope="session")
def pubsub_emulator():
    
    os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    yield
   

@pytest.fixture(scope="session", autouse=True)
def create_topics(pubsub_emulator):
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    for key, topic_name in TOPICS.items():
        topic_path = publisher.topic_path(PROJECT, topic_name)
        try:
            publisher.create_topic(request={"name": topic_path})
            print(f"Topic created: {topic_path}")
        except Exception as e:
            print(f"Topic exists or error: {e}")

        sub_name = SUBS[topic_name]
        subscription_path = subscriber.subscription_path(PROJECT, sub_name)
        try:
            subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            print(f"Subscription created: {subscription_path}")
        except Exception as e:
            print(f"Subscription exists or error: {e}")

    time.sleep(2)  