from fastapi import Depends, FastAPI
from pydantic import BaseModel

from faststream.kafka.fastapi import KafkaRouter, Logger

router = KafkaRouter("0.0.0.0:9092")

class Incoming(BaseModel):
    m: dict

def call():
    return True

@router.subscriber("test")
@router.publisher("response")
async def hello(m: Incoming, logger: Logger, d=Depends(call)):
    logger.info(m)
    return {"response": "Hello, Kafka!"}

@router.get("/")
async def hello_http():
    return "Hello, HTTP!"

app = FastAPI(lifespan=router.lifespan_context)
app.include_router(router)