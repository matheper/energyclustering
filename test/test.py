# -*- coding: utf-8 -*-
import unittest
import json
from tornado.testing import AsyncHTTPTestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import drop_database
from sqlalchemy_utils import database_exists

# import app
from app import Application
from handlers.signal import SignalHandler
from utils import parseSignal


class TestSignalParse(unittest.TestCase):

    def test_text_to_json(self):
        with open('test/signal.txt') as txt_file:
            signal_string = txt_file.read()
        txt_file.close()

        parsed_json = parseSignal(signal_string)

        with open('test/signal.json') as json_file:
            signal_json = json.load(json_file)
        json_file.close()

        self.assertEqual(parsed_json, signal_json)


class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        return createApp()

    def test_app_running(self):
        app = self.get_app()
        assert app is not None

    def test_signal_post(self):
        with open('test/signal.txt') as txt_file:
            signal_string = txt_file.read()
        txt_file.close()
        headers = {"Content-Type": "text/plain"}
        response = self.fetch(
            '/signal',
            method='POST',
            headers=headers,
            body=signal_string,
        )
        self.assertEqual(response.code, 201)
        response_body = json.loads(response.body.decode())
        self.assertEqual(response_body.get('id'), 1)


def createApp():
    db_engine = create_engine(
        "postgresql://postgres:postgres@127.0.0.1:3306/test",
        echo=False
    )
    if database_exists(db_engine.url):
        drop_database(db_engine.url)
    create_database(db_engine.url)
    db_session = sessionmaker(bind=db_engine)
    app = Application(engine=db_engine, session=db_session)
    app.session = db_session
    app.create_database()
    return app


if __name__ == '__main__':
    unittest.main()
