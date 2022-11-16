import asyncio

import eds


async def main():
    async with eds.Session() as session:
        periods = await session.list_()
        for period in periods:
            print(period)


asyncio.run(main())
