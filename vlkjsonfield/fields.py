# -*- coding: utf-8 -*-

import json
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder

import datetime
import re
from decimal import Decimal

from django.db import models


class VLKJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, datetime.time):
            return o.strftime("%H:%M:%S")
        return super(VLKJSONEncoder, self).default(o)


def json_decoder(j):
    result = []
    for k, v in j.items():
        if isinstance(v, basestring):
            result1 = re.match(r'(\d{2,4})-(\d{1,2})-(\d{1,2})', v)
            result2 = re.match(r'.*\s(\d{1,2}):(\d{1,2}):(\d{1,2})', v)
            if result1 and result2:
                year = int(result1.group(1))
                month = int(result1.group(2))
                day = int(result1.group(3))
                hour = int(result2.group(1))
                min = int(result2.group(2))
                sec = int(result2.group(3))
                v = datetime.datetime(year, month, day, hour, min, sec)
            if result1 and not result2:
                year = int(result1.group(1))
                month = int(result1.group(2))
                day = int(result1.group(3))
                v = datetime.date(year, month, day)
            if not result1 and result2:
                hour = int(result2.group(1))
                min = int(result2.group(2))
                sec = int(result2.group(3))
                v = datetime.time(hour, min, sec)
        if isinstance(v, dict):
            v = json_decoder(v)
        result.append((k, v))
    return dict(result)


class VLKJSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, basestring):
            if value.strip() == "":
                return None
            else:
                return JSONDecoder(object_hook=json_decoder).decode(json.loads(value))
        else:
            return value

    def get_prep_value(self, value):
        if not isinstance(value, dict):
            return value
        else:
            return VLKJSONEncoder().encode(json.dumps(value, cls=VLKJSONEncoder))

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fields\.VLKJSONField"])
except ImportError:
    pass
