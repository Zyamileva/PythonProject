import asyncio
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)
QUEUE_MAX_SIZE = 10


async def producer(queue):
    """Produce tasks and add them to a queue.

    Args:
        queue: The asyncio queue to add tasks to.

    Returns:
        None
    """

    try:
        for i in range(5):
            await asyncio.sleep(1)
            await queue.put(i)
            logging.info(f"task added: {i}")
    except asyncio.CancelledError as e:
        logging.error(f"An error occurred in the producer: {e}")


async def consumer(queue, consumer_id: int) -> None:
    """Consume tasks from a queue.

    Args:
        queue: The asyncio queue to consume tasks from.
        consumer_id: An identifier for the consumer.

    Returns:
        None
    """

    try:
        while True:
            task = await queue.get()
            if task is None:
                break
            logging.info(f"Task {task} taken by Consumer {consumer_id}")
            await asyncio.sleep(2)
            queue.task_done()
    except asyncio.CancelledError:
        logging.error(f"Consumer {consumer_id} was canceled.")
    finally:
        logging.info(f"Consumer {consumer_id} finished.")


async def main():
    """Orchestrate producers and consumers.

    This coroutine sets up and manages the interaction between a producer and multiple consumers using an asyncio.Queue. It starts a producer and multiple consumers, waits for the producer to finish, signals the consumers to stop, and waits for them to complete.

    Args:
        None

    Returns:
        None
    """

    n = 2
    queue = asyncio.Queue(maxsize=QUEUE_MAX_SIZE)

    producers = [asyncio.create_task(producer(queue))]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(n)]

    await asyncio.gather(*producers)

    for _ in consumers:
        await queue.put(None)

    await asyncio.gather(*consumers)
    logging.info("All tasks completed.")


asyncio.run(main())
