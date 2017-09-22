# -*- coding: utf-8 -*-
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import MeanShift

from tornado.options import options
from sqlalchemy import and_

from models import Signal


def getSignals(session, last_signal_id):
    initial_id = last_signal_id - options.sample_lenght
    signals = session.query(Signal).filter(and_(
        Signal.id > initial_id,
        Signal.id <= last_signal_id,
    ))
    return signals


def getData(signals):
    data = []
    for signal in signals:
        data.append([
            signal.power_active,
            signal.power_reactive,
            signal.power_appearent,
            signal.line_current,
            signal.line_voltage,
            signal.peaks[0],
            signal.peaks[1],
            signal.peaks[2],
        ])
    return data


def classifySignal(application, last_signal_id):
    session = application.session()
    signals = getSignals(session, last_signal_id)
    data = getData(signals)
    n_samples = min(options.sample_lenght // 2, 200)
    bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=n_samples)
    ms = MeanShift(bandwidth=bandwidth, cluster_all=False, bin_seeding=True)
    labels = ms.fit_predict(data)
    for signal, label in zip(signals, labels):
        signal.label = int(label)
    session.commit()
