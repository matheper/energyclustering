# -*- coding: utf-8 -*-
from tornado.web import URLSpec as url

from handlers.signal import SignalHandler
from handlers.report import AllReportHandler
from handlers.report import PowerAverageHandler
from handlers.report import SignalByClusterHandler
from handlers.report import SignalReportHandler


url_handlers = [
    url(r'/signal', SignalHandler),
    url(r'/report$', AllReportHandler),
    url(r'/report/(?P<signal_id>\d+$)', SignalReportHandler),
    url(r'/average', PowerAverageHandler),
    url(r'/distribution', SignalByClusterHandler),
]
