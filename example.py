import asyncio

import eds


async def main():
    for period in await eds.list_():
        print(period)


asyncio.run(main())
