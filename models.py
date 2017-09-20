# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Signal(Base):
    __tablename__ = 'signal'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('device.id'))
    alarms_coil_revesed = Column(String(20), nullable=False)
    power_active = Column(Integer, nullable=False)
    power_reactive = Column(Integer, nullable=False)
    power_appearent = Column(Integer, nullable=False)
    line_current = Column(Float, nullable=False)
    line_voltage = Column(Float, nullable=False)
    line_phase = Column(String(20), nullable=False)
    peaks = Column(ARRAY(Integer), nullable=False)
    fft_re = Column(ARRAY(Integer), nullable=False)
    fft_img = Column(ARRAY(Integer), nullable=False)
    utc_time = Column(DateTime, nullable=False)
    hz = Column(Float, nullable=False)
    wifi_strength = Column(Integer, nullable=False)
    dummy = Column(Integer, nullable=False)
    label = Column(Integer, nullable=True)
    device = relationship("Device")

    def __init__(self, data):
        self.device_id = data.get('Device ID')
        self.alarms_coil_revesed = data.get('Alarms').get('CoilRevesed')
        self.power_active = data.get('Power').get('Active')
        self.power_reactive = data.get('Power').get('Reactive')
        self.power_appearent = data.get('Power').get('Appearent')
        self.line_current = data.get('Line').get('Current')
        self.line_voltage = data.get('Line').get('Voltage')
        self.line_phase = data.get('Line').get('Phase')
        self.peaks = data.get('Peaks')
        self.fft_re = data.get('FFT Re')
        self.fft_img = data.get('FFT Img')
        utc_time = data.get('UTC Time')
        self.utc_time = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S')
        self.hz = data.get('hz')
        self.wifi_strength = data.get('WiFi Strength')
        self.dummy = data.get('Dummy')

    def to_dict(self):
        response = {}
        response = {
            'id': self.id,
            'Device': {
                'ID': self.device.id,
                'Fw': self.device.fw,
                'Evt': self.device.evt,
            },
            'Alarms': {'CoilRevesed': self.alarms_coil_revesed},
            'Power': {
                'Active': self.power_active,
                'Reactive': self.power_reactive,
                'Appearent': self.power_appearent,
            },
            'Line': {
                'Current': self.line_current,
                'Voltage': self.line_voltage,
                'Phase': self.line_phase,
            },
            'Peaks': self.peaks,
            'FFT Re': self.fft_re,
            'FFT Img': self.fft_img,
            'UTC Time': '{}-{}-{} {}:{}:{}'.format(
                self.utc_time.year,
                self.utc_time.month,
                self.utc_time.day,
                self.utc_time.hour,
                self.utc_time.minute,
                self.utc_time.second
            ),
            'hz': self.hz,
            'WiFi Strength': self.wifi_strength,
            'Dummy': self.dummy,
        }
        return response

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=False)
    fw = Column(Integer, nullable=False)
    evt = Column(Integer, nullable=False)

    def __init__(self, data):
        self.id = data.get('ID')
        self.fw = data.get('Fw')
        self.evt = data.get('Evt')


metadata = Base.metadata


def create_all(engine):
    metadata.create_all(engine)
