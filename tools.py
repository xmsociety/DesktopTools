"""
Some Tools For Coder

author: Ian Vzs
website: https://github.com/IanVzs/Halahayawa
Last edited: 10 03 2021
"""
import time
import json
import hashlib
from datetime import datetime


def json_loads(str_data):
    try:
        return json.loads(str_data)
    except:
        return {}


def json_dumps(data, ensure_ascii=False):
    try:
        data = json.dumps(data, ensure_ascii=ensure_ascii)
    except:
        pass
    return data


def datetime2str(data, fmt="%Y-%m-%d %H:%M:%S"):
    result = ''
    if data and isinstance(data, datetime):
        result = data.strftime(fmt)
    return result


def str2datetime(data, fmt="%Y-%m-%d %H:%M:%S"):
    result = None
    if data and isinstance(data, str):
        result = datetime.strptime(data, fmt)
    return result


def datetime2int(data, unit='s'):
    result = 0
    if data and isinstance(data, str) and len(data) == len("2021-01-18 14:55:00"):
        data = str2datetime(data)
    if data and isinstance(data, datetime):
        result = int(time.mktime(data.timetuple()))
    return result


def count_age(str_date: str = '', dt_date: datetime = None) -> str:
    """
    根据出生年月日计算当前年龄(年月周天)
    """
    age = ''
    if str_date and len(str_date) >= len("2020-01-01"):
        try:
            str_date = str_date[:10]
            dt_date = datetime.strptime(str_date, "%Y-%m-%d")
        except:
            dt_date = None
    if dt_date:
        now = datetime.now()
        m = (now.year * 12 + now.month) - (dt_date.year * 12 + dt_date.month)
        y = m > 12 and int(m / 12)
        if y:
            age = f"{y}岁"
        elif m:
            age = f"{m}月"
        else:
            d = now.day - dt_date.day
            w = int(d / 7)
            age = w and f"{w}周" or f"{d or 1}天"
    return age


def count_ago(str_date: str = '', dt_date: datetime = None) -> str:
    """
    ret: x(秒|分钟|小时|天|周|月|年|)之前
    """
    msg = ''
    if str_date and len(str_date) >= len("2020-01-01"):
        try:
            str_date = str_date[:10]
            dt_date = datetime.strptime(str_date, "%Y-%m-%d")
        except:
            dt_date = None
    if dt_date:
        now = datetime.now()
        interval = now - dt_date
        if interval.days > 0:
            msg = msg = count_age(dt_date=dt_date)
            msg = msg.replace('岁', '年')
        elif interval.days == 0 and interval.seconds > 10:
            _s = interval.seconds
            _m = _s and int(_s / 60)
            _h = _m and int(_m / 60)

            _str_s = (_s and f"{_s}秒")
            _str_m = (_m and f"{_m}分钟" or _str_s)
            _str_h = (_h and f"{_h}小时" or _str_m)
            msg = _str_s and _str_m and _str_h

        else:
            msg = '刚刚'
        msg = f"{msg}之前" if "刚刚" not in msg else msg
    return msg


def time_now(ty: str = 'str'):
    now = datetime.now()
    if ty == "str":
        return datetime2str(now)
    else:
        return now


def md5_convert(string):
    """
    计算字符串md5值
    :param string: 输入字符串
    :return: 字符串md5
    """
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()


def check_keys(keys, must=None) -> bool:
    if must and set(keys) > set(must):
        return True
    elif must:
        return False
    else:
        return True

