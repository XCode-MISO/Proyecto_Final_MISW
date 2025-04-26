"""
Fixtures y preparación de Pub/Sub emulador para los tests E2E.
"""
import os, time, subprocess, pytest
from google.cloud import pubsub_v1

EMULATOR_HOST = "localhost:8681"
PROJECT       = "test-proj"
TOPICS        = {
    "products": "inventarios-products",
    "stock":    "inventarios-stock",
}
SUBS = {
    "inventarios-products": "sub-products",
    "inventarios-orders": "sub-orders",
}

# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def pubsub_emulator():
    os.environ["PUBSUB_EMULATOR_HOST"] = EMULATOR_HOST
    proc = subprocess.Popen(
        ["gcloud", "beta", "emulators", "pubsub", "start",
         f"--host-port={EMULATOR_HOST}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(3)          # espera arranque
    yield
    proc.terminate()

# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def create_topics(pubsub_emulator):
    publisher  = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    for topic in TOPICS.values():
        topic_path = publisher.topic_path(PROJECT, topic)
        sub_path   = subscriber.subscription_path(PROJECT, SUBS[topic])
        try:
            publisher.create_topic(request={"name": topic_path})
        except Exception:
            pass
        try:
            subscriber.create_subscription(
                request={"name": sub_path, "topic": topic_path}
            )
        except Exception:
            pass
    yield