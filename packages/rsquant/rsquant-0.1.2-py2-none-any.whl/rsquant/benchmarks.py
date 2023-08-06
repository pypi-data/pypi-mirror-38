#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pandas as pd
import requests
from logbook import Logger
import os

logger = Logger('benchmark')

BENCH_URL = 'http://www.rstone.com/api/v1/chart?symbol={}'
host = os.getenv('QUANT_HOST')
if host != None:
	BENCH_URL = host + '/api/v1/chart?symbol={}'
	del host

def get_benchmark_returns(symbol):
    """
    Get a Series of benchmark returns from rsAPI associated with `symbol`.
    Default is `sh000001`.

    Parameters
    ----------
    symbol : str
        Benchmark symbol for which we're getting the returns.

    The data is provided by rsAPI (https://rstone.com/), and we can
    get up to 30 years worth of data.
    """
    logger.info(('Download benchmark from {url!r}'),
        url=BENCH_URL.format(symbol))
    r = requests.get(
        BENCH_URL.format(symbol)
    )
    data = r.json()

    df = pd.DataFrame(data)

    df.index = pd.DatetimeIndex(df['date'])
    df = df['close']

    return df.sort_index().tz_localize('UTC').pct_change(1).iloc[1:]
