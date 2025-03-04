import asyncio
import logging

from aiohttp import web


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def home_route(request):
    """Handle requests to the home route.

    This function serves as a simple handler for requests made to the application's home route.  It returns a "Hello, World!" message.

    Args:
        request: The request object.

    Returns:
        web.Response: A response object containing the "Hello, World!" message.
    """

    logging.info("Home: request")
    return web.Response(text="Hello, World!")


async def slow_route(request):
    """Handle requests to the slow route.

    This function simulates a slow operation by pausing for 5 seconds before returning a response. It's useful for testing or demonstrating asynchronous behavior.

    Args:
        request: The request object.

    Returns:
        web.Response: A response object containing the "Operation completed" message.
    """

    logging.info("Slow: request before sleep")
    await asyncio.sleep(5)
    logging.info("Slow: request after sleep")
    return web.Response(text="Operation completed")


app = web.Application()
app.add_routes([web.get("/", home_route), web.get("/slow", slow_route)])


if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8080)
