import aiohttp
import asyncio
import difflib
from dotenv import load_dotenv
import os


from solver import Sudoku

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
    res = None

    try:
        res = await get_puzzle("medium")
    except Exception as e:
        print(e)

    if not res:
        return

    puzzle = res["puzzle"]
    solution = res["solution"]

    output = Sudoku.new_from_string(puzzle).solve()

    print(f"solution: {solution}")
    print(f"  answer: {output}")

    if output != solution:
        print(
            f"    diff: {"".join([
            "^" if solution[i] != output[i] else " " for i in range(len(solution))
        ])}"
        )
        print("NO MATCH")
    else:
        print("CORRECT SOLUTION")


if __name__ == "__main__":
    asyncio.run(main())
