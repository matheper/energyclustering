# -*- coding: utf-8 -*-
from tornado.web import URLSpec as url

import app
from handlers.signal import SignalHandler


url_handlers = [
    url(r'/signal', SignalHandler, dict(
            session=app.db_session,
    )),
]
