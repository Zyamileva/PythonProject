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
    """Run the main program.

    This coroutine executes the slow_task with a timeout of 5 seconds.  If the task does not complete within the timeout period, a TimeoutError is raised.

    Args:
        None

    Returns:
        None
    """

    try:
        await asyncio.wait_for(slow_task(), timeout=5)
    except asyncio.TimeoutError:
        logging.info("Время ожидания вышло.")


asyncio.run(main())
