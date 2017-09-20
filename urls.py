# -*- coding: utf-8 -*-
from tornado.web import URLSpec as url

from handlers.signal import SignalHandler


url_handlers = [
    url(r'/signal', SignalHandler),
]
