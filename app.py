# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists


from settings import settings
import urls
import models


connection_str = "postgres://{}:{}@{}/{}".format(
    options.pg_user, options.pg_password,
    options.pg_host, options.pg_database,
)

db_engine = create_engine(connection_str)
if not database_exists(db_engine.url):
    create_database(db_engine.url)
db_session = sessionmaker(bind=db_engine)


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session')
        self.session.configure(bind=db_engine)
        tornado.web.Application.__init__(self, urls.url_handlers, **settings)

    def create_database(self):
        models.create_all(db_engine)


def main():
    app = Application(session=db_session)
    app.create_database()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
