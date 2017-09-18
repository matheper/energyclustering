# -*- coding: utf-8 -*-
from tornado.options import define

define("port", default=8888, help="run on the given port", type=int)


settings = dict(
    debug=True,
    autoreload=True,
)
