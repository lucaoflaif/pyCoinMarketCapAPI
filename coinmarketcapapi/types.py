"""This module has all classes needed that help the package's structure
"""

import datetime as dt

class Coin:
    """Coin class
    """
    def __init__(self, coin_id, name, symbol, rank, price_usd, price_btc, volume_usd_24h,
                 market_cap_usd, available_supply, total_supply, max_supply,
                 percent_change_1h, percent_change_24h, percent_change_7d,
                 last_updated, price_converted=None, volume_24h_converted=None,
                 market_cap_converted=None):

        # direct string to int cast isn't possible
        self.rank = int(rank)

        self.symbol = symbol
        self.name = name
        self.coin_id = coin_id

        self.price_usd = float(price_usd)
        self.price_btc = float(price_btc)
        self.volume_usd_24h = float(volume_usd_24h)
        self.market_cap_usd = float(market_cap_usd)
        self.available_supply = float(available_supply)
        self.total_supply = float(total_supply)
        if max_supply: #  max supply can be None from APIs
            self.max_supply = float(max_supply)
        if percent_change_1h:
            self.percent_change_1h = float(percent_change_1h)
        if percent_change_24h:
            self.percent_change_24h = float(percent_change_24h)
        if percent_change_7d:
            self.percent_change_7d = float(percent_change_7d)

        self.last_updated = self._format_last_updated_date(last_updated)

        if price_converted:
            self.price_converted = float(price_converted)
        if volume_24h_converted:
            self.price_converted = float(volume_24h_converted)
        if market_cap_converted:
            self.price_converted = float(market_cap_converted)

    def __str__(self):
        return "%(coin_name)s (%(symbol)s)" % {
            'coin_name': self.name,
            'symbol': self.symbol
        }

    def _format_last_updated_date(self, timestamp):
        timestamp = int(timestamp)
        return dt.datetime.fromtimestamp(timestamp)

class Global:
    """Global class
    """
    def __init__(self, total_market_cap_usd, total_24h_volume_usd,
                 bitcoin_percentage_of_market_cap, active_currencies,
                 active_assets, active_markets, last_updated,
                 total_market_cap_eur=None, total_24h_volume_eur=None):

        self.total_market_cap_usd = total_market_cap_usd
        self.total_24h_volume_usd = total_24h_volume_usd
        self.bitcoin_percentage_market_cap = bitcoin_percentage_of_market_cap
        self.active_currencies = active_currencies
        self.active_assets = active_assets
        self.active_markets = active_markets

        self.last_updated = self._format_last_updated_date(last_updated)

        if total_market_cap_eur:
            self.total_market_cap_eur = total_market_cap_eur
        if total_24h_volume_eur:
            self.total_24h_volume_eur = total_24h_volume_eur

    @staticmethod
    def _format_last_updated_date(timestamp):
        timestamp = int(timestamp)
        return dt.datetime.fromtimestamp(timestamp)
