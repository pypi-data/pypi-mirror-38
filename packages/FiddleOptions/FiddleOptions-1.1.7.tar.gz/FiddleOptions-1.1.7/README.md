# swagger-client
Fixed generated code from Swagger Codegen https://github.com/swagger-api/swagger-codegen)

## Requirements

Python 2.7 and 3.4+c

## Installation 
### pip install 
```sh
pip install fiddleoptions
```

Then import the package:
```sh
import fiddle_options
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install 
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import swagger_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# create an instance of the API class
api_instance = swagger_client.FiddleApi()
id = 'id_example' # str | 

try:
    # Deletes Fiddle with specified id
    api_instance.delete_fiddle(id)
except ApiException as e:
    print("Exception when calling FiddleApi->delete_fiddle: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://localhost/mercury/*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FiddleApi* | [**delete_fiddle**](docs/FiddleApi.md#delete_fiddle) | **DELETE** /fiddle/delete/{id} | Deletes Fiddle with specified id
*FiddleApi* | [**get_fiddle**](docs/FiddleApi.md#get_fiddle) | **GET** /fiddle/load/{id} | Returns the Fiddle with specified id
*FiddleApi* | [**get_fiddle_list**](docs/FiddleApi.md#get_fiddle_list) | **GET** /fiddle/{userId}/list | Returns the list of Fiddles for the specified user
*FiddleApi* | [**get_position_legs**](docs/FiddleApi.md#get_position_legs) | **POST** /fiddle/position/legs | Returns all options contracts that the specified options position is consisted of
*FiddleApi* | [**get_trade_from_tos_string**](docs/FiddleApi.md#get_trade_from_tos_string) | **POST** /fiddle/position/fromTOSString | Creates a list of positions from a list of trades specified in ThinkOrSwim format
*FiddleApi* | [**save_fiddle**](docs/FiddleApi.md#save_fiddle) | **POST** /fiddle/{userId}/save | Saves a new Fiddle or updates an existing one
*MarketdataApi* | [**get_equity_quote**](docs/MarketdataApi.md#get_equity_quote) | **GET** /marketdata/equity/{name} | Returns equity quotes for each trading day for the given ticker and time period
*MarketdataApi* | [**get_expirations**](docs/MarketdataApi.md#get_expirations) | **GET** /marketdata/option-chain/expirations/{name} | Returns expirations for the given symbol and trading date
*MarketdataApi* | [**get_horizontally_sliced_option_chain_by_delta**](docs/MarketdataApi.md#get_horizontally_sliced_option_chain_by_delta) | **GET** /marketdata/option-chain/{name}/horizontal-slice-by-delta | Returns horizontal slice of option chain for the given symbol, option type, trading dates, expiration, and the delta strike range
*MarketdataApi* | [**get_horizontally_sliced_option_chain_by_strike**](docs/MarketdataApi.md#get_horizontally_sliced_option_chain_by_strike) | **GET** /marketdata/option-chain/{name}/horizontal-slice-by-strike | Returns horizontal slice of option chain for the given symbol, option type, trading dates, expiration, and the strike range
*MarketdataApi* | [**get_option_chain**](docs/MarketdataApi.md#get_option_chain) | **GET** /marketdata/option-chain/{name} | Returns option chain for the given symbol, trading date, and expiration date
*MarketdataApi* | [**get_server_time**](docs/MarketdataApi.md#get_server_time) | **GET** /marketdata/servertime | Get the current server time
*MarketdataApi* | [**get_trading_dates**](docs/MarketdataApi.md#get_trading_dates) | **GET** /marketdata/tradingdates/{symbol} | Returns actual trading days in specified from/to date range
*MarketdataApi* | [**get_vertically_sliced_option_chain_by_delta**](docs/MarketdataApi.md#get_vertically_sliced_option_chain_by_delta) | **GET** /marketdata/option-chain/{name}/vertical-slice-by-delta | Returns vertical slice of option chain for the given symbol, option type, trading date, expiration, and the delta strike range
*MarketdataApi* | [**get_vertically_sliced_option_chain_by_strike**](docs/MarketdataApi.md#get_vertically_sliced_option_chain_by_strike) | **GET** /marketdata/option-chain/{name}/vertical-slice-by-strike | Returns vertical slice of option chain for the given symbol, option type, trading date, expiration, and the strike range
*MarketdataApi* | [**get_volatility_skew**](docs/MarketdataApi.md#get_volatility_skew) | **GET** /marketdata/iv-skew | Returns volatility skews for the given trading symbol, the expiration and the observation dates
*MarketdataApi* | [**search_tickers**](docs/MarketdataApi.md#search_tickers) | **GET** /marketdata/tickers | Searchs for symbols in the system with an optional query parameter. If query parameter is not used all symbols are returned
*TradeserviceApi* | [**calculate_decomposed_pn_l**](docs/TradeserviceApi.md#calculate_decomposed_pn_l) | **POST** /tradeservice/dpnlCalculator | Returns the P&amp;L timeline decomposed by greeks for the given trade and the specified time range
*TradeserviceApi* | [**calculate_historical_pn_l**](docs/TradeserviceApi.md#calculate_historical_pn_l) | **POST** /tradeservice/histpnlCalculator | Returns the P&amp;L timeline for the given trade and the specified time range
*TradeserviceApi* | [**calculate_historical_value**](docs/TradeserviceApi.md#calculate_historical_value) | **POST** /tradeservice/histvalueCalculator | Returns the historical dollar denominated value for the given trade and the time window
*TradeserviceApi* | [**calculate_instant_decomposed_pn_l**](docs/TradeserviceApi.md#calculate_instant_decomposed_pn_l) | **POST** /tradeservice/instantdpnlCalculator | Returns the greek decomposed P&amp;L for the given trade and the time window
*TradeserviceApi* | [**calculate_pn_l**](docs/TradeserviceApi.md#calculate_pn_l) | **POST** /tradeservice/pnlCalculator | Returns the the t+0 curve and expiration PnL curve for the given trade


## Documentation For Models

 - [DataPoint](docs/DataPoint.md)
 - [DateValueDataPoint](docs/DateValueDataPoint.md)
 - [DateValueDataPointDouble](docs/DateValueDataPointDouble.md)
 - [EquityQuote](docs/EquityQuote.md)
 - [Fiddle](docs/Fiddle.md)
 - [Greeks](docs/Greeks.md)
 - [IVSkew](docs/IVSkew.md)
 - [IVSkewDataPoint](docs/IVSkewDataPoint.md)
 - [OptionChain](docs/OptionChain.md)
 - [OptionContract](docs/OptionContract.md)
 - [OptionLeg](docs/OptionLeg.md)
 - [PnL](docs/PnL.md)
 - [PnLCurve](docs/PnLCurve.md)
 - [Position](docs/Position.md)
 - [Ticker](docs/Ticker.md)
 - [Trade](docs/Trade.md)
 - [Butterfly](docs/Butterfly.md)
 - [LongCallVerticalSpread](docs/LongCallVerticalSpread.md)
 - [LongPutVerticalSpread](docs/LongPutVerticalSpread.md)
 - [OptionSingle](docs/OptionSingle.md)
 - [Spread](docs/Spread.md)
 - [Straddle](docs/Straddle.md)
 - [Strangle](docs/Strangle.md)
 - [VerticalSpread](docs/VerticalSpread.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author



