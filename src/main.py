from fastapi import Depends, FastAPI
from pydantic import BaseModel

from faststream.kafka.fastapi import KafkaRouter, Logger

KAFKA_LOCAL = "kafka:9092"
KAFKA_AWS = 'example:9092'

router = KafkaRouter(KAFKA_AWS)


@router.subscriber("test")
@router.publisher(topic="response")
@router.publisher(topic="hippo")
async def hello(msg_body: dict):
    print({'msg': msg_body['msg']})

@router.subscriber("response")
async def response():
    print("response!!!")


@router.subscriber("hippo")
async def hippo():
    print("hippo!!!")


@router.get(path="/")
async def hello_http():
    return "Hello, HTTP!"


@router.post(path="/send")
async def send_message(name: str):
    await router.broker.publish(
        message={"msg": f"Hello, {name}!"},
        topic="test"
    )
    return {"status": "message sent"}


app = FastAPI(lifespan=router.lifespan_context)
app.include_router(router)
