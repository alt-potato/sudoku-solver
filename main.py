import aiohttp
import asyncio
from dotenv import load_dotenv
import os

import solver as s

load_dotenv()
API_KEY = os.getenv("YOUDOSUDOKU_API_KEY")


async def get_puzzle(difficulty: str = "hard") -> dict:
    """Get a random puzzle from the youdosudoku API.

    Throws an exception if the request fails.

    see: https://www.youdosudoku.com/
    """

    API_URL = "https://www.youdosudoku.com/api/"

    body = {
        "difficulty": difficulty,
        "solution": True,
        "array": False,
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, json=body, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error {response.status}: {await response.text()}")


async def main():
    puzzle = None

    try:
        puzzle = await get_puzzle("easy")
    except Exception as e:
        print(e)
    



if __name__ == "__main__":
    asyncio.run(main())
