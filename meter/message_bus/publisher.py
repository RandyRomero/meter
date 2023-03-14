import logging
import typing as tp
from asyncio import AbstractEventLoop
from json import dumps

import aio_pika
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

logger = logging.getLogger("meter.message_bus.publisher")

logging.getLogger("aiormq").setLevel(logging.WARNING)
logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


class RabbitClient:
    def __init__(self) -> None:
        self._connection: AbstractRobustConnection
        self._channel: AbstractChannel

    async def connect(self, login: str, password: str, host: str, port: int, loop: AbstractEventLoop) -> None:
        # for production code it is better to use connection pool and
        # channel pool, but for such a tiny app there is not point in doing
        # that
        self._connection = await connect_robust(
            login=login, password=password, host=host, port=port, loop=loop, timeout=5
        )
        self._channel = await self._connection.channel()

    async def publish(
        self,
        data: dict[str, tp.Any],
        exchange_name: str,
        routing_key: str,
        exchange_type: ExchangeType = ExchangeType.DIRECT,
    ) -> None:
        """Publishes data to rabbit."""
        exchange = await self._channel.declare_exchange(
            exchange_name,
            durable=True,
            type=exchange_type.value,
        )

        logger.info(
            "Publishing a new message. Exchange name: %s. Routing key: %s. Data: %s",
            exchange_name,
            routing_key,
            str(data),
        )

        await exchange.publish(
            aio_pika.Message(dumps(data, default=str).encode()),
            routing_key,
        )
