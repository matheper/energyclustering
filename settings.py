# -*- coding: utf-8 -*-
from tornado.options import define
from tornado.options import options

define("port", default=8888, help="run on the given port", type=int)
define("pg_host", default="127.0.0.1:5432", help="database host")
define("pg_database", default="ecluster", help="database name")
define("pg_user", default="postgres", help="database user")
define("pg_password", default="postgres", help="database password")

conn_str = "postgres://{}:{}@{}/{}".format(
    options.pg_user, options.pg_password,
    options.pg_host, options.pg_database,
)
define("connection_str", default=conn_str, help="database connection srt")

settings = dict(
    debug=True,
    autoreload=True,
)
