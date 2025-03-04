import asyncio
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def producer(queue):
    """Produce data and add it to a queue.

    This coroutine generates a sequence of numbers (0-4) with a 1-second delay between each, and adds them to the provided queue.  It simulates a data producer in a producer-consumer pattern.

    Args:
        queue: The asyncio.Queue instance to add data to.

    Returns:
        None
    """

    for i in range(5):
        await asyncio.sleep(1)
        await queue.put(i)
        logging.info(f"task added: {i}")


async def consumer(queue, consumer_id: int) -> None:
    """Consume data from a queue.

    This coroutine retrieves tasks from the given queue and processes them, simulating a consumer in a producer-consumer pattern.  It continues until it receives a None value, indicating the end of the data stream.

    Args:
        queue: The asyncio.Queue instance to consume data from.
        consumer_id (int): An identifier for the consumer.

    Returns:
        None
    """

    while True:
        task = await queue.get()
        if task is None:
            break
        await asyncio.sleep(2)
        logging.info(f"Еhe task was taken away {task}. Consumer {consumer_id}")
        queue.task_done()


async def main():
    """Orchestrate producers and consumers.

    This coroutine sets up and manages the interaction between a producer and multiple consumers using an asyncio.Queue. It starts a producer and multiple consumers, waits for the producer to finish, signals the consumers to stop, and waits for them to complete.

    Args:
        None

    Returns:
        None
    """

    n = 2
    queue = asyncio.Queue()

    producers = [asyncio.create_task(producer(queue))]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(n)]

    await asyncio.gather(*producers)

    for _ in consumers:
        await queue.put(None)

    await asyncio.gather(*consumers)


asyncio.run(main())
