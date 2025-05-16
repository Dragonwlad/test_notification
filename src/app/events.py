# """Module with fastapi events."""
#
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
#
# from src.redis_client import get_redis_client
# from src.telegram_sdk.client import client_pool
#
# scheduler = AsyncIOScheduler()
#
#
# async def startup_event() -> None:
#     """Handle FastAPI startup event.
#
#     Initializes Redis connection.
#     Initializes key manager, add rotation job.
#     """
#
#     await get_redis_client()
#
#
# async def shutdown_event() -> None:
#     """Handle FastAPI shutdown event.
#
#     Closes the Redis connection.
#     """
#     for k, (ts, tg_client) in list(client_pool.items()):
#         await tg_client.disconnect()
#
#     redis_client = await get_redis_client()
#     await redis_client.close()
