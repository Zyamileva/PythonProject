import asyncio
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def slow_task():
    """Simulate a slow-running task.

    This coroutine simulates a task that takes a significant amount of time to complete (10 seconds in this case).
    It can be used to demonstrate asynchronous operations and cancellation.

    Args:
        None

    Returns:
        None
    """

    logging.info("Начало выполнения задания...")
    try:
        await asyncio.sleep(10)
        logging.info("Задание выполнено!")
    except asyncio.CancelledError:
        logging.info("Задание не было выполнено.")


async def main():
    """Run a slow task with a timeout.

    Returns:
        None
    """
    task = asyncio.create_task(slow_task())
    try:
        await asyncio.wait_for(task, timeout=5)
    except asyncio.TimeoutError:
        task.cancel()
        logging.info("Время ожидания вышло.")


asyncio.run(main())
