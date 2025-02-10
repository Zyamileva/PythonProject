import asyncio
from typing import Dict, Any


class AsyncFetcher:
    @staticmethod
    async def fetch(url: str) -> Dict[str, Any]:
        await asyncio.sleep(5)
        return {"url": url, "status": 200, "id": 5}


async def main():
    fetcher = AsyncFetcher()
    result = await fetcher.fetch("https://example.com/api")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
