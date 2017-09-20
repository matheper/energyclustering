# -*- coding: utf-8 -*-
from tornado.options import define

define("port", default=8888, help="run on the given port", type=int)
define("pg_host", default="127.0.0.1:5432", help="database host")
define("pg_database", default="ecluster", help="database name")
define("pg_user", default="postgres", help="database user")
define("pg_password", default="postgres", help="database password")


settings = dict(
    debug=True,
    autoreload=True,
)
