# Energy Data Service

MicroPython Library for the Energy Data Service

## Command line interface

Get Danish electricity prices for the next 24 hours

```python
import asyncio

import eds


async def main():
    async with eds.Session() as session:
        periods = await session.list_()
        for period in periods:
            print(period)


asyncio.run(main())
```

```
2022.11.17 23:00  24 øre
2022.11.17 22:00  30 øre
2022.11.17 21:00  28 øre
...
```
