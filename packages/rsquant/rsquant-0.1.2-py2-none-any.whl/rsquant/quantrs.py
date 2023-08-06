"""
Module for building a complete daily dataset from RStone Quant's dataset.
"""
from io import BytesIO
import tarfile
from zipfile import ZipFile

from click import progressbar
from logbook import Logger
import pandas as pd
import requests
from six.moves.urllib.parse import urlencode
from six import iteritems
from trading_calendars import register_calendar_alias

from zipline.utils.deprecate import deprecated
import zipline.data.bundles as bundles
import numpy as np
import os

log = Logger(__name__)

ONE_MEGABYTE = 1024 * 1024
QUANT_DATA_URL = 'http://www.rstone.com/api/v1/'
host = os.getenv('QUANT_HOST')
if host != None:
    QUANT_DATA_URL = host + '/api/v1/'


def format_metadata_url(filen, api_key):
    """ Build the query URL for RStone Quant Prices metadata.
    """
    query_params = [('api_key', api_key)]

    return QUANT_DATA_URL + filen + '?' + urlencode(query_params)


def load_data_table(file,
                    index_col,
                    show_progress=False):
    """ Load data table from zip file provided by RStone Quant.
    """
    with ZipFile(file) as zip_file:
        file_names = zip_file.namelist()
        assert len(file_names) == 1, "Expected a single file from Quandl."
        wiki_prices = file_names.pop()
        with zip_file.open(wiki_prices) as table_file:
            if show_progress:
                log.info('Parsing raw data.')
            data_table = pd.read_csv(
                table_file,
                parse_dates=['date'],
                index_col=index_col,
                #engine='c',
                #header=None,
                usecols=[
                    'symbol',
                    'date',
                    'open',
                    'high',
                    'low',
                    'close',
                    'volume',
                    'turnover',
                ],
                dtype={
                    'volume':np.int64,
                    'turnover':np.float64,
                    'open':np.float,
                    'high':np.float,
                    'low':np.float,
                    'close':np.float,
                }
            )
    return data_table


def fetch_data_table(api_key,
                     show_progress,
                     retries):
    """ Fetch Prices data table from Stone Quant
    """
    for _ in range(retries):
        try:
            urlS = format_metadata_url('symbols.csv', api_key)
            if show_progress:
                log.info(('Downloading metadata from {url!r}'), url=urlS)

            metadata = pd.read_csv(
                urlS,
                parse_dates=['start_date','end_date','auto_close_date'],
                index_col=None,
                #header=None,
                encoding='gbk',
                usecols=[
                    'symbol',
                    'name',
                    'start_date',
                    'end_date',
                    'auto_close_date',
                    'exchange',
                ],
            )
            # Extract symbols from metadata and download zip file.
            table_url = format_metadata_url('daily.csv', api_key)
            if show_progress:
                raw_file = download_with_progress(
                    table_url,
                    chunk_size=ONE_MEGABYTE,
                    label="Downloading daily Prices table from QuantRS"
                )
            else:
                raw_file = download_without_progress(table_url)

            return metadata, load_data_table(
                file=raw_file,
                index_col=None,
                show_progress=show_progress,
            )

        except Exception:
            log.exception("Exception raised reading Quandl data. Retrying.")

    else:
        raise ValueError(
            "Failed to download Quandl data after %d attempts." % (retries)
        )


def parse_splits(data, show_progress):
    if show_progress:
        log.info('Parsing split data.')

    data['split_ratio'] = 1.0 / data.split_ratio
    data.rename(
        columns={
            'split_ratio': 'ratio',
            'date': 'effective_date',
        },
        inplace=True,
        copy=False,
    )
    return data


def parse_dividends(data, show_progress):
    if show_progress:
        log.info('Parsing dividend data.')

    data['record_date'] = data['declared_date'] = data['pay_date'] = pd.NaT
    data.rename(
        columns={
            'ex_dividend': 'amount',
            'date': 'ex_date',
        },
        inplace=True,
        copy=False,
    )
    return data


def parse_pricing_and_vol(data,
                          sessions,
                          symbol_map):
    for asset_id, symbol in iteritems(symbol_map):
        asset_data = data.xs(
            symbol,
            level=1
        ).reindex(
            sessions.tz_localize(None)
        ).fillna(0.0)
        yield asset_id, asset_data


@bundles.register('quantrs')
def quantrs_bundle(environ,
                  asset_db_writer,
                  minute_bar_writer,
                  daily_bar_writer,
                  adjustment_writer,
                  calendar,
                  start_session,
                  end_session,
                  cache,
                  show_progress,
                  output_dir):
    """
    quandl_bundle builds a daily dataset using RStone Quant's Prices dataset.

    For more information on RStone Quant's API and how to obtain an API key,
    please visit https://docs.quandl.com/docs#section-authentication
    """
    api_key = environ.get('QUANT_API_KEY')
    if api_key is None:
        raise ValueError(
            "Please set your QUANT_API_KEY environment variable and retry."
        )
    #print("url: ", QUANT_DATA_URL)
    asset_metadata, raw_data = fetch_data_table(
        api_key,
        show_progress,
        environ.get('QUANT_DOWNLOAD_ATTEMPTS', 5)
    )
    asset_db_writer.write(asset_metadata)

    symbol_map = asset_metadata.symbol
    sessions = calendar.sessions_in_range(start_session, end_session)

    raw_data.set_index(['date', 'symbol'], inplace=True)
    daily_bar_writer.write(
        parse_pricing_and_vol(
            raw_data,
            sessions,
            symbol_map
        ),
        show_progress=show_progress
    )

    adjustment_writer.write(splits=None, dividends=None)
    """
    raw_data.reset_index(inplace=True)
    raw_data['symbol'] = raw_data['symbol'].astype('category')
    raw_data['sid'] = raw_data.symbol.cat.codes
    adjustment_writer.write(
        splits=parse_splits(
            raw_data[[
                'sid',
                'date',
                'split_ratio',
            ]].loc[raw_data.split_ratio != 1],
            show_progress=show_progress
        ),
        dividends=parse_dividends(
            raw_data[[
                'sid',
                'date',
                'ex_dividend',
            ]].loc[raw_data.ex_dividend != 0],
            show_progress=show_progress
        )
    )
    """


def download_with_progress(url, chunk_size, **progress_kwargs):
    """
    Download streaming data from a URL, printing progress information to the
    terminal.

    Parameters
    ----------
    url : str
        A URL that can be understood by ``requests.get``.
    chunk_size : int
        Number of bytes to read at a time from requests.
    **progress_kwargs
        Forwarded to click.progressbar.

    Returns
    -------
    data : BytesIO
        A BytesIO containing the downloaded data.
    """
    resp = requests.get(url, stream=True)
    resp.raise_for_status()

    total_size = int(resp.headers['content-length'])
    data = BytesIO()
    with progressbar(length=total_size, **progress_kwargs) as pbar:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            data.write(chunk)
            pbar.update(len(chunk))

    data.seek(0)
    return data


def download_without_progress(url):
    """
    Download data from a URL, returning a BytesIO containing the loaded data.

    Parameters
    ----------
    url : str
        A URL that can be understood by ``requests.get``.

    Returns
    -------
    data : BytesIO
        A BytesIO containing the downloaded data.
    """
    resp = requests.get(url)
    resp.raise_for_status()
    return BytesIO(resp.content)
