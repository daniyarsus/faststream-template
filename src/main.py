from fastapi import Depends, FastAPI
from pydantic import BaseModel

from faststream.kafka.fastapi import KafkaRouter, Logger

router = KafkaRouter("kafka:9092")


@router.subscriber("test")
@router.publisher(topic="response")
@router.publisher(topic="hippo")
async def hello():
    print("hellooooo!!!")


@router.subscriber("response")
async def response():
    print("response!!!")


@router.subscriber("hippo")
async def hippo():
    print("hippo!!!")


@router.get(path="/")
async def hello_http():
    return "Hello, HTTP!"


@router.get(path="/send")
async def send_message():
    await router.broker.publish(
        message={"msg": "Hello, Kafka!"},
        topic="test"
    )
    return {"status": "message sent"}


app = FastAPI(lifespan=router.lifespan_context)
app.include_router(router)
