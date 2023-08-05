from tornado.options import options, define
from .json_utils import dumps
import asyncio, aioredis
import logging
import redis

async def connect():
    loop = asyncio.get_event_loop()
    redis = await aioredis.create_redis(options.redis_url, loop=loop)
    logging.info("connect to redis: %s", options.redis_url)
    return redis


async def pool():
    loop = asyncio.get_event_loop()
    pool = await aioredis.create_pool(options.redis_url,
                    minsize=5, maxsize=10, loop=loop)
    logging.info("pool to redis: %s", options.redis_url)
    return pool
