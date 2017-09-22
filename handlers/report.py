# -*- coding: utf-8 -*-
import json
import tornado
from sqlalchemy import func

from models import Signal


class SignalReportHandler(tornado.web.RequestHandler):

    def get(self, signal_id=None):
        try:
            session = self.application.session()
            data = session.query(Signal).filter_by(id=signal_id)
            self.write(json.dumps(data.first().to_dict()))
        except:
            msg = "Could not find: %s" % self.request.body
            raise tornado.web.HTTPError(400, msg)


class AllReportHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            session = self.application.session()
            data = session.query(Signal).all()
            self.write(json.dumps([signal.to_dict() for signal in data]))
        except:
            raise tornado.web.HTTPError(500)


class PowerAverageHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            session = self.application.session()
            query = session.query(
                Signal.label,
                func.avg(Signal.power_active)
            ).group_by(Signal.label)
            results = []
            for label, value in query.all():
                results.append(
                    {'label':label, 'active power average': float(value)}
                )
            self.write(json.dumps(results))
        except:
            raise tornado.web.HTTPError(500)


class SignalByClusterHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            session = self.application.session()
            query = session.query(
                Signal.label,
                func.count(Signal.id)
            ).group_by(Signal.label)
            results = []
            for label, value in query.all():
                results.append({'label':label, 'associated events': value})
            self.write(json.dumps(results))
        except:
            raise tornado.web.HTTPError(500)
