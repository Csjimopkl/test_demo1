# -*- coding: utf-8 -*-
# @Author  : zhangjiada.zjd
# @Time    : 2023/2/24 18:58
# @Email   : zhangjiada.zjd@alibaba-inc.com
# @Function:

import datetime
import json
import time
import traceback
import requests


# from tests.conf.config import *

"""
备注：由于get请求限制了查询参数，因此在api.py中get请求相关的接口中，将params的取值统一调整为
params=kwargs.get("search")，这样search在函数中不定义时，会拿到一个None，不影响查询；如果需要给search赋值，
需要在对应的接口请求处加上search的字典内
"""

def http_post(url, params=None, skip=True, **kwargs):
    headers = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    if kwargs.get("header") is not None:
        headers = kwargs.get("header")
    print(u"\n[Info]: POST {0}".format(url))
    print(u"[Info]: {0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print(u"[Info]: Payload \n{0}".format(json.dumps(params, indent=4, ensure_ascii=False, separators=(',', ': '))))
    if kwargs.get("verify") is not None:
        res = requests.post(url=url, headers=headers, json=params, verify=False)
    else:
        res = requests.post(url=url, headers=headers, json=params)

    print(u"[Info]: 0.5s !!! Wait for this creation to finish")
    time.sleep(0.5)
    try:
        json.dumps(res.json(), indent=4, separators=(',', ': '))

    except ValueError:
        msg = traceback.format_exc()
        print(res.status_code)
        return res.status_code, msg
    else:
        if params and not params.get("print_tag"):
            print(u"[Info]: response \n{0}".format(
                json.dumps(res.json(), ensure_ascii=False, indent=4, separators=(',', ': '))))
        return res.status_code, res.json()


def status_check_call(url, payload, **kwargs):
    header = {
        "Content-Type": "application/json"
    }
    url = u'{0}/client/account.status.check?cver=2.4.7&df=json&gt=ng&os=ios&ver=1.0'.format(url)
    status_code, data = http_post(url=url, params=payload, header=header)
    return status_code, data


def login_call(url, payload, **kwargs):
    header = {
        "Content-Type": "application/json"
    }
    url = u'{0}/client/account.loginByPassword?cver=2.4.7&df=json&gt=ng&os=android&ver=1.0'.format(url)
    status_code, data = http_post(url=url, params=payload, header=header)
    return status_code, data
