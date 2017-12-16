import datetime as dt

class Coin:
    def __init__(self, id, name, rank, price_usd, price_btc, 24h_volume_usd,
                    market_cap_usd, available_supply, total_supply, max_supply,
                    percent_change_1h, percent_change_24h, percent_change_7d,
                    last_updated, price_converted = None, 24h_volume_converted = None, 
                    market_cap_converted = None):
        
        
        self.rank = int(rank)
        
        self.name = name
        self.id = id

        self.price_usd = float(price_usd)
        self.price_btc = float(price_usd)
        self.24h_volume_usd = float(24h_volume_usd)
        self.market_cap_usd = float(market_cap_usd)
        self.available_supply = float(available_supply)
        self.total_supply = float(total_supply)
        self.max_supply = float(max_supply)
        self.percent_change_1h = float(percent_change_1h)
        self.percent_change_24h = float(percent_change_24h)
        self.percent_change_7d = float(percent_change_7d)
        
        self.last_updated = self._format_last_updated_date(last_updated)

        if price_converted:
            self.price_converted = float(price_converted)
        if 24h_volume_converted:
            self.price_converted = float(24h_volume_converted)
        if market_cap_converted:
            self.price_converted = float(market_cap_converted)



    def _format_last_updated_date(self, timestamp):
        return dt.datetime.fromtimestamp(timestamp)

class Coins:
    def __init__(self):
        pass

    def __iter__(self):
        yield 1