# -*- coding: utf-8 -*-
import re


def parseSignal(signal_string):
    clean_signal = signal_string.strip()
    labels = re.compile("[a-zA-Z]*\w+ ?(?=[a-zA-Z])\w+:").findall(clean_signal)
    values = re.compile(" ?[a-zA-Z]*\w+ ?(?=[a-zA-Z])\w+: ?").split(
        clean_signal
    )[1:]
    signal_dict = {}
    for key, value in zip(labels, values):
        key = key.replace(':', '')
        signal_dict[key] = parseValue(value)
    return signal_dict


def parseValue(value):
    splited = [v for v in value.split(';') if v]
    if '=' in value:
        v_dict = {}
        for item in splited:
            k, v = item.split('=')
            k = k.replace(' ', '')
            v_dict[k] = convertTextToNumber(v)
        return v_dict
    if len(splited) == 1:
        return convertTextToNumber(splited[0])
    return [convertTextToNumber(t) for t in splited]


def convertTextToNumber(text):
    try:
        s = ''.join([s for s in text if s.isdigit() or s in ['-', '.', ',']])
        return float(s) if '.' in s or 'e' in s.lower() else int(s)
    except:
        return text
