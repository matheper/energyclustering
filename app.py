# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from redis import StrictRedis

from settings import settings
import urls
import models


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        self.engine = kwargs.pop('engine')
        self.session = kwargs.pop('session')
        self.redis = kwargs.pop('redis')
        self.session.configure(bind=self.engine)
        tornado.web.Application.__init__(self, urls.url_handlers, **settings)

    def create_database(self):
        models.create_all(self.engine)


def main():
    db_engine = create_engine(options.connection_str)
    if not database_exists(db_engine.url):
        create_database(db_engine.url)
    db_session = sessionmaker(bind=db_engine)

    st_redis = StrictRedis(
        host=options.redis_host,
        port=options.redis_port,
        db=options.redis_db
    )

    app = Application(engine=db_engine, session=db_session, redis=st_redis)
    app.create_database()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
