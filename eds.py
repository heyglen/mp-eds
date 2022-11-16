import datetime
import statistics

import uaiohttpclient as aiohttp

LOG_DATE_FORMAT = "%Y.%m.%d %H:%M:%S"


class RelativeCost:
    expensive = 1
    mid_priced = 2
    cheap = 3
    unknown = 4


class Period:
    def __init__(
        self,
        when,
        price,
        currency="dkk",
        currency_unit="øre",
        hour_unit="kWh",
        relative_price=RelativeCost.unknown,
    ):
        self.when = when
        self.price = price
        self.currency = currency
        self.currency_unit = currency_unit
        self.hour_unit = hour_unit
        self.relative_price = relative_price

    def __str__(self):
        when = self.when.strftime("%Y.%m.%d %H:%M")
        return f"{when} {self.price:3} {self.currency_unit}"


class PriceArea:
    west_of_great_belt = "DK1"
    east_of_great_belt = "DK2"


class Eds:
    version = "1.0.0"

    def __init__(self, price_area=PriceArea.east_of_great_belt):
        self._price_area = price_area
        self._session = session

    async def list_(self):
        response = await aiohttp.get(
            "https://api.energidataservice.dk/dataset/Elspotprices"
        )
        data = await response.json()

        periods = list()
        for record in data["records"]:
            price_area = record["PriceArea"]
            if price_area != self._price_area:
                continue
            timestamp = datetime.datetime.strptime(
                record["HourDK"], "%Y-%m-%dT%H:%M:%S"
            )
            period = Period(
                when=timestamp,
                price=round(record["SpotPriceDKK"] / 10),
            )
            periods.append(period)

        cheap, expensive = statistics.quantiles([p.price for p in periods], n=3)

        for period in periods:
            if period.price < cheap:
                period.relative_price = RelativeCost.cheap
            elif cheap <= period.price < expensive:
                period.relative_price = RelativeCost.mid_priced
            elif expensive <= period.price:
                period.relative_price = RelativeCost.expensive

        return periods
