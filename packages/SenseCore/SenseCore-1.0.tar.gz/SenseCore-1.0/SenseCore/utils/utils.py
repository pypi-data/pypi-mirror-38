import numpy
import json
import logging
import datetime
import time

logger = logging.getLogger('django')

def log_info(msg, *args, **kwargs):
    logger.info(msg,*args,**kwargs)

def log_error(msg, *args, **kwargs):
    logger.error(msg,*args,**kwargs)

def log_exception(msg, *args, exc_info=True, **kwargs):
    logger.exception(msg, *args, exc_info, **kwargs)

def dump_json(data):
    return json.dumps(data,ensure_ascii=False)

def load_json(data):
    try:
        return json.loads(data)
    except:
        return None

def convert_timestamp_to_str(time,format='%Y-%m-%d'):
    return datetime.datetime.fromtimestamp(time).strftime(format)

def build_model_list(items,type='list'):
    list = []
    for item in items:
        list.append(item.to_json(type))
    return list

def get_current_millisecond():
    return int(round(time.time() * 1000))

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj)
        else:
            return super(NumpyEncoder, self).default(obj)