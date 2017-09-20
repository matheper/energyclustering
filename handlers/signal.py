# -*- coding: utf-8 -*-
import json
import tornado

from utils import parseSignal
from models import Signal
from models import Device


class SignalHandler(tornado.web.RequestHandler):

    def post(self):
        try:
            session = self.application.session()
            signal_data = parseSignal(self.request.body.decode())
            device = Device(signal_data.get('Device'))
            if not session.query(Device).filter_by(id=device.id).first():
                session.add(device)
                session.commit()
            signal_data['Device ID'] = device.id
            signal = Signal(signal_data)
            session.add(signal)
            session.commit()
            self.set_status(201)
            self.write(json.dumps(signal.to_dict()))
        except:
            msg = "Could not decode: %s" % self.request.body
            raise tornado.web.HTTPError(400, msg)
