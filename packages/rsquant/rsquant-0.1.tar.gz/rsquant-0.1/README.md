# rsquant`
A Python library of exchange calendars and data bundles meant to be used with [Zipline](https://github.com/quantopian/zipline).

| Exchange                        | ISO Code | Country     | Version Added | Exchange Website (English)                              |
| ------------------------------- | -------- | ----------- | ------------- | ------------------------------------------------------- |
| Shanghai Security Exchange      | XSHG     | China       | 1.x           | http://www.sse.com.cn/                                  |
| Shanghai Futures Exchange       | XSGE     | China       | 1.x           | http://www.shfe.com.cn/                                 |

Calendars marked with an asterisk (*) have not yet been released.

Note that exchange calendars are defined by their [ISO-10383 market identifier code](https://www.iso20022.org/10383/iso-10383-market-identifier-codes).

## Usage
```python
import rsquant

# US Stock Exchanges (includes NASDAQ)
us_calendar = get_calendar('XNYS')
# London Stock Exchange
london_calendar = get_calendar('XLON')
# Toronto Stock Exchange
toronto_calendar = get_calendar('XTSE')
# Tokyo Stock Exchange
tokyo_calendar = get_calendar('XTKS')
# Frankfurt Stock Exchange
frankfurt_calendar = get_calendar('XFRA')
sse_calendar = get_calendar('SSE')

# US Futures
us_futures_calendar = get_calendar('us_futures')
# Chicago Mercantile Exchange
cme_calendar = get_calendar('CMES')
# Intercontinental Exchange
ice_calendar = get_calendar('IEPA')
# CBOE Futures Exchange
cfe_calendar = get_calendar('XCBF')
# Shanghai Futures Exchange
shfe_calendar = get_calendar('SHFE')
```
