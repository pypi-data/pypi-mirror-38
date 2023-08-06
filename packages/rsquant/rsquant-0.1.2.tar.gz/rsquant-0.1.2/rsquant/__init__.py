#
# Copyright 2018 Quantopian, Inc.
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

from trading_calendars import (
    clear_calendars,
    deregister_calendar,
    get_calendar,
    register_calendar,
    register_calendar_alias,
    register_calendar_type,
)
import zipline

name = "rsquant"
__all__ = [
    'clear_calendars',
    'deregister_calendar',
    'get_calendar',
    'register_calendar',
    'register_calendar_alias',
    'register_calendar_type',
]

from .exchange_calendar_xsge import XSGEExchangeCalendar
from .exchange_calendar_xshg import XSHGExchangeCalendar

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
from .quantrs import quantrs_bundle

xsge = XSGEExchangeCalendar()
#register_calendar('XSGE', XSGEExchangeCalendar)
register_calendar('XSGE', xsge)
register_calendar_alias('SHFE', 'XSGE')
register_calendar_alias('DCE', 'XSGE')
register_calendar_alias('XDCE', 'XSGE')
register_calendar_alias('CZCE', 'XSGE')
register_calendar_alias('XZCE', 'XSGE')
register_calendar_alias('XCFE', 'XSGE')
register_calendar_alias('CFFEX', 'XSGE')
xshg = XSHGExchangeCalendar()
#register_calendar('XSHG', XSHGExchangeCalendar, True)
register_calendar('XSHG', xshg, True)
register_calendar_alias('SSE', 'XSHG')
register_calendar_alias('SHSE', 'XSHG')
register_calendar_alias('XSHE', 'XSHG')
register_calendar_alias('SZSE', 'XSHG')
