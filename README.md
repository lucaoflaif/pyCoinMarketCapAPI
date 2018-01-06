# pyCoinMarketCapAPI

[![Build Status](https://travis-ci.org/lucaoflaif/pyCoinMarketCapAPI.svg?branch=master)](https://travis-ci.org/lucaoflaif/pyCoinMarketCapAPI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a935cced37274464855a235173b809fb)](https://www.codacy.com/app/lucaoflaif/pyCoinMarketCapAPI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lucaoflaif/pyCoinMarketCapAPI&amp;utm_campaign=Badge_Grade)
![PyPI](https://img.shields.io/pypi/status/pyCoinMarketCapAPI.svg)
![PyPI](https://img.shields.io/pypi/pyversions/pyCoinMarketCapAPI.svg)
![PyPI](https://img.shields.io/pypi/v/pyCoinMarketCapAPI.svg)
[![PyPI](https://img.shields.io/pypi/l/pyCoinMarketCapAPI.svg)]()

pyCoinMarketCapAPI is a python interface for <https://coinmarketcap.com> APIs, It supports a cache, and a dynamic timezone mechanism.

## Installation

* Installation from source (requires git):

``` bash
git clone <https://github.com/lucaoflaif/pyCoinMarketCapAPI.git>
cd pyCoinMarketCapAPI
python setup.py install
```

* Installation from `pip`:

``` bash
pip install pyCoinMarketCapAPI
```

## Getting started

First, import our class with:

``` python
import coinmarketcapapi
```

Then, we have to create an istance of our class:

``` python
coin_apis = coinmarketcapapi.CoinMarketCapAPI()
```

*See [Class' constructor parameters](#class-constructor-parameters) for the class' parameters.*

Okay, let's call the server:

``` python
coin_apis.send_request()
```

Thanks to this method we filled our class with new data and the Cache mechanism will be activated (See [Cache mechanism](#cache-mechanism)), call this method is **necessary** for the first time in order to have data to work with.

*You can pass to the `send_request()` method all the parameters allowed by the official APIs (See [Public methods](#public-methods))*

Then, make our first call:

``` python
coin = coin_apis.coin(coin_name='bitcoin')
```

*See [Public methods](#public-methods) (highly recommended)*

So easy! Check out what `coin` is:

``` python
>>> print (type(coin))
<class 'coinmarketcapapi.types.Coin'>
```

Our coin variable is an istance of the `Coin` class. Now, if we want to know (for example) its change in 1h (in percentage):

``` python
>>> print (coin.percent_change_1h)
-1.0
```

*See [Types](#types) (highly recommended)*

## Prerequisites

Just be sure you have installed python 3.6.* or higher.

## Documentation

### Class constructor parameters

The parameter we can pass through `CoinMarketCapAPI` class is `max_request_per_minute`, see the table below for further information.

| Parameter | Type | Optional | Function
| :---         |     :---:      |          :---: | ---:
| `max_request_per_minute`   | Int     | No, but initialized to 9    | Define the max number of requests to the APIs server per minute (See [Cache mechanism](#cache-mechanism))

### Public methods

* `coin(coin_name="string")`

You should use this method to get an istance of `Coin` class (*See [Types](#types)*) of one coin (specified through `coin_name` parameter)

* `coins()`

You should use this method to get info about all available coins. It'll return a generator object of Coin istances of all coins:

```python
>>> print (type(coin_apis.coins()))
<class 'generator'>
```

that you can iterate:

```python
>>> for coin_istance in coin_apis.coins():
...     print (coin_istance.coin_id, coin_istance.symbol, coin_istance.price_usd, coin_istance.percent_change_24h)

bitcoin BTC 16861.1 -2.47
ethereum ETH 866.568 6.05
bitcoin-cash BCH 3672.79 8.72
ripple XRP 1.01362 31.25
litecoin LTC 328.665 -0.57
iota MIOTA 5.12173 -4.6
cardano ADA 0.489473 -3.38
dash DASH 1511.09 14.38
...
```

(*See [Types](#types) to know which and how to get data from the `Coin` istance*)

Optionally, you can use:

* `get_response()`

If only a "ticker" type request is cached, this method returns the response converted from json to a python list:

``` python
>>> print (coin_apis.get_response())
[{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC', 'rank': '1', 'price_usd': '16861.1', 'price_btc': '1.0', '24h_volume_usd': '18988100000.0', 'market_cap_usd': '282504560613', 'available_supply': '16754812.0', 'total_supply': '16754812.0', 'max_supply': '21000000.0', 'percent_change_1h': '-1.0', 'percent_change_24h': '-2.47', 'percent_change_7d': '1.59', 'last_updated': '1513851256'}, {'id': 'ethereum', 'name': 'Ethereum', 'symbol': 'ETH', 'rank': '2', 'price_usd': '866.568', 'price_btc': '0.0515602', '24h_volume_usd': '3621040000.0', 'market_cap_usd': '83602326421.0', 'available_supply': '96475206.0', 'total_supply': '96475206.0', 'max_supply': None, 'percent_change_1h': '0.07', 'percent_change_24h': '6.05', 'percent_change_7d': '19.97', 'last_updated': '1513851256'}, ... ]
>>> print (type(coin_apis.get_response()))
<class 'list'>
```

If only a "global" type request is cached, this method returns the response converted from json to a python dict:

```python
>>> print (coin_apis.get_response()
{'active_assets': 464,
 'active_currencies': 910,
 'active_markets': 7397,
 'bitcoin_percentage_of_market_cap': 43.34,
 'last_updated': 1514481559,
 'total_24h_volume_usd': 31313412913.0,
 'total_market_cap_usd': 559006768817.0}
>>> print (type(coin_apis.get_response()))
<class 'dict'>
```

If we have both, we have to pass a `data_type` parameter through the function:

```python
coin_apis.get_response(data_type='ticker') # for ticker cached data
coin_apis.get_response(data_type='global') # for global cached data
```

* `send_request()`

The `send_request()` method is used to retrieve new data from the official coinmarketcap server: the first parameter is `endpoint` initialised to `ticker`, it accepts all parameters described by the [official doc](https://coinmarketcap.com/api/).

| Endpoint |Function | Example
| :----: | :----: | :----:
| `ticker` | Retrieve specific currency | `endpoint="ticker"`
| `global` | Retrieve global data | `endpoint="global"`

The table above explain how endopint are organised

| Parameter | Optional | Example | Endpoint |Function
| :---:         |    :---:  |    :---: | :----: |:---:
| `convert`   | Yes     | `convert="EUR"`  | `ticker`, `global` | From doc: ```(string) convert - return price, 24h volume, and market cap in terms of another currency. Valid values are:  "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"```
| `start` | Yes | `start=5` | `ticker` |From doc: ```(int) start - return results from rank [start] and above```
| `limit` | Yes | `limit=10` | `ticker` |From doc: ```(int) limit - return a maximum of [limit] results (default is 100, use 0 to return all results)```

The table above explain how parameters are organised

The built function should be something like:

```python
send_request() # endpoint is default 'ticker', no additional params
# or
send_request(limit=5) # ticker endpoint with limit parameter
# or
send_request(endpoint="global") # global endpoint with no additional params
# or
send_request(endpoint='global', convert="EUR") # global endpoint with convert parameter
```

### Types

* class `Coin`

An istance of the `Coin` class is returned for every coin's info requested (as explained in [Public methods](#public-methods) section), you can access the information of the coin through the class' attributes as explained in the table below:

| Attribute name |Type | Info type
| :----: | :----: | :----:
| `coin_id` | String | Coin id |
| `name` | String | Coin name |
| `symbol` | String | Coin symbol |
| `rank` | Int | Coin rank |
| `price_usd` | Float | Coin price (in USD) |
| `price_btc` | Float | Coin price (in BTB) |
| `volume_usd_24h` | Float | Volume in the last 24h (in USD) |
| `market_cap_usd` | Float | Market Cap (in USD) |
| `available_supply` | Float | Available supply |
| `total_supply` | Float if present else None | Total supply |
| `max_supply` | Float | Max supply |
| `percent_change_1h` | Float if present else None | Value change in the last hour (percentage) |
| `percent_change_24h` | Float if present else None | Value change in the 24h (percentage) |
| `percent_change_7d` | Float if present else None | Value change in the last week (percentage) |
| `last_updated` | datetime object if present else None | Last data update of API server |
| `price_converted` | Float if present else None | Price converted (in the currency specified, see `send_request()` in [Public methods](#public-methods)) |
| `volume_24h_converted` | Float if present else None | Volume in the last 24h converted (in the currency specified, see `send_request()` in [Public methods](#public-methods)) |
| `market_cap_converted` | Float if present else None | Market CAP converted in the currency specified, see `send_request()` in [Public methods](#public-methods)) |

`total_supply`, `percent_change_7d`, `percent_change_1h`, `percent_change_24h` could be `None` because API could send `null` as their value.

`price_converted`, `volume_24h_converted`, `market_cap_converted` could be `None` if no `convert` parameter has been passed to `send_request()` [public method](#public-methods).

### Cache mechanism

One of the features of this library is the Cache Mechanism. Simply, as explained in [Class constructor parameters](#class-constructor-parameters), you can specify how many requests per minute you want to send to the server, you can call the `send_request()` [plublic method](#public-methods) as many times as you want: the mechanism will automatically choose if return the cached response, or call the server for new and fresh data, don't worry, the data will be cleverly managed and refreshed with regular time cadence (respecting, of course, the preset limit)

## Running the tests

* You can automatically run the tests *(Recommended choice)* running:

``` bash
python setup.py test
```

(It'll provide to install dependencies and run all the tests)

* You can manually run the tests simply running:

``` bash
$ for file in $(ls tests); do
    if [[ $file != __* ]]; then
        python tests/$file
    fi
done
...
----------------------------------------------------------------------
Ran 3 tests in 28.044s

OK
...
```

(it requires the `unittest` python package included in the [Python Standard Library](https://docs.python.org/3/library/index.html))

### Break down into end to end tests

* cache_test.py

This test simply will test if the cache mechanism works correctly.

* coins_select_mechanism_test.py

This test simply will test if the public methods (and other elements that'll be explained later) will return the expected and correct result(s). See the [tests files](tests/) for further info!

The output of the tests should be something like:

``` bash
$ python tests/cache_test.py
...
----------------------------------------------------------------------
Ran 3 tests in 27.253s

OK

$ python tests/coins_select_mechanism_test.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK

# and so on
```

## Authors

* **Luca Di Vita** - [GitHub](https://github.com/lucaoflaif/), [Telegram](https://t.me/lucaoflaif)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

### Let me know if you are using this APIs and I'll add your project here
