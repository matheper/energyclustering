# -*- coding: utf-8 -*-
import unittest
import json
from tornado.testing import AsyncHTTPTestCase
from tornado.options import define
from tornado.options import options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import drop_database
from sqlalchemy_utils import database_exists
from redis import StrictRedis

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


class BaseTest(AsyncHTTPTestCase):

    def get_app(self):
        self.app = createApp()
        return self.app

    def tearDown(self):
        self.app.session.close_all()


class TestApp(BaseTest):

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


class TestSignalClassification(BaseTest):

    def load_sample(self):
        define("sample_lenght", 30)
        with open('test/signal.txt') as txt_file:
            signal_string = txt_file.read()
        txt_file.close()
        with open('test/signal2.txt') as txt_file:
            signal_string2 = txt_file.read()
        txt_file.close()
        with open('test/signal3.txt') as txt_file:
            signal_string3 = txt_file.read()
        txt_file.close()
        headers = {"Content-Type": "text/plain"}
        for i in range(10):
            response = self.fetch(
                '/signal',
                method='POST',
                headers=headers,
                body=signal_string,
            )
            response = self.fetch(
                '/signal',
                method='POST',
                headers=headers,
                body=signal_string2,
            )
            response = self.fetch(
                '/signal',
                method='POST',
                headers=headers,
                body=signal_string3,
            )

    def test_signal_classification(self):
        self.load_sample()
        response = self.fetch('/report', method='GET')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode())
        labels = [signal.get('Label') for signal in data]
        self.assertEqual(labels.count(0), 10)
        self.assertEqual(labels.count(1), 10)
        self.assertEqual(labels.count(2), 10)

    def test_one_signal_classification(self):
        self.load_sample()
        response = self.fetch('/report/1', method='GET')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode())
        self.assertEqual(data.get('Label'), 0)

    def test_active_power_average(self):
        self.load_sample()
        response = self.fetch('/average', method='GET')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode())
        self.assertCountEqual(data, [
            {'label': 1, 'active power average': 189.0},
            {'label': 0, 'active power average': 289.0},
            {'label': 2, 'active power average': 0.0}
        ])

    def test_associated_events(self):
        self.load_sample()
        response = self.fetch('/distribution', method='GET')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode())
        self.assertCountEqual(data, [
            {'label': 1, 'associated events': 10},
            {'label': 2, 'associated events': 10},
            {'label': 0, 'associated events': 10}
        ])


def createApp():
    db_engine = create_engine(
        "postgresql://{}:{}@{}/test".format(
            options.pg_user,
            options.pg_password,
            options.pg_host,
        ),
        echo=False
    )
    if database_exists(db_engine.url):
        drop_database(db_engine.url)
    create_database(db_engine.url)
    db_session = sessionmaker(bind=db_engine)
    redis = StrictRedis(
        host=options.redis_host,
        port=options.redis_port,
        db=1,
    )
    redis.set('signal_count', 0)
    app = Application(engine=db_engine, session=db_session, redis=redis)
    app.session = db_session
    app.create_database()
    return app


if __name__ == '__main__':
    unittest.main()
