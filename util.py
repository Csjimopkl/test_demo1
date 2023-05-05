# -*- coding:utf-8 -*-
import pathmatcher

import test_pytest

import json
import sys
import payload
import datetime
import requests
import time
import traceback
import xlrd


def test03_mobile_detail(caseId="813433875904624119"):
    #工单状态查看(详情查看)
    url = "https://daily-ieu-cs-front.qookkagames.com/api/case/detail?ver=1.0&df=json"
    data = payload.mobile_detail_show
    data["caseId"] = caseId
    data["token"] = test_pytest.mobile_token
    data["accountToken"] = test_pytest.mobile_token
    res = requests.post(url,json=data)
    res = res.json()
    status = res["code"]
    return res,status


