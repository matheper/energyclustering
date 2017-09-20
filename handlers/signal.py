# -*- coding: utf-8 -*-
import tornado

from utils import parseSignal

from models import Signal
from models import Device


class SignalHandler(tornado.web.RequestHandler):

    def initialize(self, session):
        self.session = session()

    def post(self):
        try:
            signal_data = parseSignal(self.request.body.decode())
            device = Device(signal_data.get('Device'))
            if not self.session.query(Device).filter_by(id=device.id).first():
                self.session.add(device)
                self.session.commit()
            signal_data['Device ID'] = device.id
            signal = Signal(signal_data)
            self.session.add(signal)
            self.session.commit()
        except:
            msg = "Could not decode: %s" % self.request.body
            raise tornado.web.HTTPError(400, msg)
