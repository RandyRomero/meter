import asyncio
import logging
import random
from asyncio import AbstractEventLoop

from meter.message_bus.publisher import RabbitClient
from meter.settings import settings

EXCHANGE_NAME = "METER"
ROUTING_KEY = "meter_value"

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(lineno)s:%(message)s", level=logging.DEBUG)

logger = logging.getLogger("meter")


def get_meter_value() -> int:
    """Example of implementation."""
    new_meter_value = random.randint(0, 9001)
    logger.info("New meter value: %d", new_meter_value)
    return new_meter_value


async def main(event_loop: AbstractEventLoop) -> None:
    rabbitmq = RabbitClient()
    await rabbitmq.connect(
        settings.RABBIT_LOGIN,
        settings.RABBIT_PASSWORD,
        settings.RABBIT_HOST,
        settings.RABBIT_PORT,
        event_loop,
    )

    while True:
        meter_value = get_meter_value()

        await rabbitmq.publish(data={"value": meter_value}, exchange_name=EXCHANGE_NAME, routing_key=ROUTING_KEY)

        await asyncio.sleep(settings.SLEEP_TIMEOUT_SECONDS)


if __name__ == "__main__":
    logger.info("Initializing...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
