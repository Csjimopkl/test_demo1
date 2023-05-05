# -*- coding:utf-8 -*-


import pytest

import payload
from account_api import *

user_accessToken = "AQZQMTExNDTKwXnGmJmiGt3/sCvP9Y/VA9M8tEwZGWRkF8fMZUt1bul+Dsk8f8hV5tOOuTmb2GjEczXz"

class TestCS:
    @classmethod
    def setup_class(self):
        print(u"\n[Info]: for setup")
        # ***************************************
        #               开始测试
        # ***************************************
        global mobile_token
        #跟踪一个工单
        global dataId

        global magic_account_url
        global caseSubmit_url
        global batchAssign_url
        global batchReply_url
        global caseEvaluate_url
        global caseAttachInfo_url
        global supplementMaterials_url
        global caseDetail_url

        magic_account_url = "https://magic-account.flysdk.cn"
        caseSubmit_url = "https://daily-ieu-cs-front.qookkagames.com/api/case/submit?ver=1.0&df=json"
        batchAssign_url = "https://daily-ieu-cs.qookkagames.com/api/workOrder/batchAssign"
        batchReply_url = "https://daily-ieu-cs.qookkagames.com/api/workOrder/batchReply"
        caseEvaluate_url = "http://daily-ieu-cs-front.qookkagames.com/api/case/evaluate?ver=1.0&df=json"
        caseAttachInfo_url = "https://daily-ieu-cs-front.qookkagames.com/api/case/attachInfo?ver=1.0&df=json"
        supplementMaterials_url = "https://daily-ieu-cs.qookkagames.com/api/workOrder/batchAskToSupplementMaterials"
        caseDetail_url = "https://daily-ieu-cs-front.qookkagames.com/api/case/detail?ver=1.0&df=json"


        """
        elif brand == 'heping':
            magic_account_url = env_config['lingXi1_magic_account']
            gangplank_url = env_config['lingXi1_gangplank']
            ds_account_url = env_config['lingXi1_ds_account']
        elif brand == 'lingXi2':
            magic_account_url = env_config['lingXi1_magic_account']
            gangplank_url = env_config['lingXi1_gangplank']
            ds_account_url = env_config['lingXi1_ds_account']
        elif brand == 'poTong':
            magic_account_url = env_config['lingXi1_magic_account']
            gangplank_url = env_config['lingXi1_gangplank']
            ds_account_url = env_config['lingXi1_ds_account']
        """
        # print(
        #     "\n*************************************"
        #     "\n[Setup Info]:"
        #     "\n** brand : {0}   "
        #     "\n** game_id : {1}   "
        #     "\n** magic_account_url : {2}   "
        #     "\n** ds_account_url : {3}   "
        #     "\n** gangplank_url : {4}   "
        #     "\n*************************************\n".format(brand, game_id,
        #                                                        magic_account_url, ds_account_url, gangplank_url)
        #)

    @pytest.mark.query
    def test01_login_phone(self):
        #登陆提单账号，获取token
        phone = '15016507212'

        # 账号状态
        check_req = payload.account_status_check_req
        check_req['data']['loginName'] = phone
        status_code, resp = status_check_call(magic_account_url, check_req)
        assert status_code == 200, "查找状态请求失败，http status code不为200"
        assert resp['state']['subCode'] == 2000000 and resp['data']['hasPassword'] == 1, "查找状态请求失败，code不为2000000" \
                                                                                         "或者hasPassword不为1 "

        # 灵犀登录
        req_data = {
            "name": phone,
            "password": "123123q",
            "areaCode": "86",
            "encrypt": 0,
            "loginType": 1
        }
        magic_req = payload.magic_login_req
        magic_req['data'] = req_data
        status_code, resp = login_call(magic_account_url, magic_req)
        assert status_code == 200, "登录接口请求失败，http status code不为200"
        assert resp['state']['subCode'] == 2000000, "登录请求失败，code不为2000000"

        # 大圣登录
        global mobile_token
        mobile_token = resp['data']['token']
        time.sleep(1)

    def test02_mobile_submit(self):
        #直接提单
        # url = "https://daily-ieu-cs-front.qookkagames.com/api/case/submit?ver=1.0&df=json"
        data = payload.submit_body_picture
        data["token"] = mobile_token
        data["accountToken"] = mobile_token
        res = requests.post(caseSubmit_url,json=data)

        res = res.json()
        status = res["code"]
        global dataId
        dataId = res["data"]
        assert "2000000" == status, "文字+图片提单失败，status不为2000000" # 断言使用Python原生assert
        assert "操作成功"== res['msg']
        time.sleep(1)

        # 工单指派
        headers = {
            "Content-Type": "application/json",
            "access_token": user_accessToken
        }
        data = payload.batch_assign
        data["workOrderIds"] = [str(dataId)]
        # url = "https://daily-ieu-cs.qookkagames.com/api/workOrder/batchAssign"
        res = requests.post(batchAssign_url, headers=headers, json=data)
        res = res.json()
        status = res["code"]
        assert "2000000" == status, "工单指派失败，status不为2000000"
        time.sleep(1)


    def test03_user_reply(self):
        #工单回复
        headers = {
            "Content-Type": "application/json",
            "access_token": user_accessToken
        }
        global dataId
        if (dataId != ""):
            # url = "https://daily-ieu-cs.qookkagames.com/api/workOrder/batchReply"
            data  = {
                "plainContent": "测试使用",
                "workOrderIds": [str(dataId)],
                "content": "<p>测试问题</p>",
                "picUrls": []
            }
            res = requests.post(batchReply_url,headers=headers,json=data)

            res = res.json()
            status = res["code"]
            assert "2000000" == status, "工单回复失败，status不为2000000" # 断言使用Python原生assert
            assert "操作成功"== res['msg']
        time.sleep(1)

    def test04_mobile_evaluate(self):
        #工单评价
        #获取工单列表：选取第一个已回复的工单
        # url = "https://daily-ieu-cs-front.qookkagames.com/api/case/list?ver=1.0&df=json"
        # data = payload.mobile_list
        # data["token"] = mobile_token
        # data["accountToken"] = mobile_token
        # res = requests.post(url, json=data)
        # res = res.json()
        # status = res["code"]
        # assert "2000000" == status, "工单列表获取失败，status不为2000000"  # 断言使用Python原生assert
        #
        # data = res["data"]
        # list = data["dataList"]
        # task_id = ""
        # for l in list:
        #     if l["status"] == "REPLIED":
        #         task_id = l["caseId"]
        #         #查看该提单有无评价
        #         res,status = test03_mobile_detail(task_id)
        #         assert "2000000" == status, "工单详情查看失败，status不为2000000"  # 断言使用Python原生assert
        #         assert "操作成功" == res['msg']
        #
        #         data_tmp = res["data"]
        #         if data_tmp[0]["evaluateScore"] == None:
        #             break
        #         else:
        #             task_id = ""
        #
        # assert task_id != "", "无符合评价条件的工单"  #无符合评价条件的提单
        global dataId
        if(dataId!=""):
            # url = "http://daily-ieu-cs-front.qookkagames.com/api/case/evaluate?ver=1.0&df=json"
            data = payload.mobile_evaluete
            data["token"] = mobile_token
            data["accountToken"] = mobile_token
            data["caseId"] = dataId
            res = requests.post(caseEvaluate_url,json=data)

            res = res.json()
            status = res["code"]
            assert "2000000" == status, "工单评价失败，status不为2000000" # 断言使用Python原生assert
            assert "操作成功"== res['msg']
        time.sleep(1)

    #@pytest.mark.skip("调试，跳过")
    def test05_mobile_additional_submit(self):
        #追加提单
        #获取工单列表：选取第一个已回复的工单
        # url = "https://daily-ieu-cs-front.qookkagames.com/api/case/list?ver=1.0&df=json"
        # data = payload.mobile_list
        # data["token"] = mobile_token
        # data["accountToken"] = mobile_token
        # res = requests.post(url, json=data)
        # res = res.json()
        # status = res["code"]
        # assert "2000000" == status, "工单列表获取失败，status不为2000000"  # 断言使用Python原生assert
        #
        # data = res["data"]
        # list = data["dataList"]
        # task_id = ""
        # for l in list:
        #     if l["status"] == "REPLIED":
        #         task_id = l["caseId"]
        #         #查看该提单有无追加提问
        #         res,status = test03_mobile_detail(task_id)
        #         assert "2000000" == status, "工单详情查看失败，status不为2000000"  # 断言使用Python原生assert
        #         assert "操作成功" == res['msg']
        #         data_tmp = res["data"]
        #         if data_tmp[0]["parentCaseId"] == "0":
        #             break
        #         else:
        #             task_id = ""
        #
        # assert task_id != ""  #无符合评价条件的提单
        global dataId
        if(dataId!=""):
            # url = "https://daily-ieu-cs-front.qookkagames.com/api/case/submit?ver=1.0&df=json"
            data = payload.mobile_additional_submit
            data["parentCaseId"] = dataId
            data["token"] = mobile_token
            data["accountToken"] = mobile_token
            res = requests.post(caseSubmit_url,json=data)

            res = res.json()
            status = res["code"]
            dataId = res["data"]
            assert "2000000" == status, "工单追加提交失败，status不为2000000" # 断言使用Python原生assert
            assert "操作成功"== res['msg']
        time.sleep(0.3)

    #@pytest.mark.skip("调试，跳过")
    def test06_mobile_append_submit(self):
        #补充材料递交
        #获取工单列表：选取第一个未回复的工单
        # url = "https://daily-ieu-cs-front.qookkagames.com/api/case/list?ver=1.0&df=json"
        # data = payload.mobile_list
        # data["token"] = mobile_token
        # data["accountToken"] = mobile_token
        # res = requests.post(url, json=data)
        # res = res.json()
        # status = res["code"]
        # assert "2000000" == status, "工单列表获取失败，status不为2000000"
        #
        # data = res["data"]
        # list = data["dataList"]
        # task_id = ""
        # for l in list:
        #     if l["status"] != "REPLIED":
        #         task_id = l["caseId"]
        #         break
        #
        # assert task_id != ""  #无符合补充材料条件的提单

        global dataId
        if(dataId!=""):
            # url = "https://daily-ieu-cs-front.qookkagames.com/api/case/attachInfo?ver=1.0&df=json"
            data = payload.mobile_append_submit
            data["caseId"] = dataId
            data["token"] = mobile_token
            data["accountToken"] = mobile_token
            res = requests.post(caseAttachInfo_url,json=data)

            res = res.json()
            status = res["code"]
            assert "2000000" == status, "补充材料提交失败，status不为2000000" # 断言使用Python原生assert
            assert "操作成功"== res['msg']
        time.sleep(1)

    #@pytest.mark.skip("调试，跳过")
    def test07_user_append_subject(self):
        #补充材料下发
        #后台获取工单列表：选取第一个未回复的工单
        headers = {
            "Content-Type": "application/json",
            "access_token": user_accessToken
        }
        # data = payload.user_get_detail
        # url = "https://daily-ieu-cs.qookkagames.com/api/workOrder/search"
        # res = requests.post(url, headers=headers, json=data)
        # res = res.json()
        # status = res["code"]
        # assert "2000000" == status, "工单列表获取失败，status不为2000000"
        #
        # data = res["data"]
        # list = data["dataList"]
        # task_id = list[0]["id"]
        # assert task_id != "", "没有未回复工单"
        global dataId
        if(dataId!=""):
            # url = "https://daily-ieu-cs.qookkagames.com/api/workOrder/batchAskToSupplementMaterials"
            data = payload.user_put_append
            list_tmp = [dataId]
            data["workOrderIds"] = list_tmp
            res = requests.post(supplementMaterials_url,headers=headers,json=data)

            res = res.json()
            status = res["code"]
            assert "2000000" == status, "下发补充材料失败，status不为2000000" # 断言使用Python原生assert
            assert "操作成功" == res['msg']

    #@pytest.mark.skip("调试，跳过")
    def test08_mobile_detail(self):
        #工单状态查看(详情查看)
        #url = "https://daily-ieu-cs-front.qookkagames.com/api/case/detail?ver=1.0&df=json"
        data = payload.mobile_detail_show
        data["caseId"] = dataId
        data["token"] = mobile_token
        data["accountToken"] = mobile_token
        res = requests.post(caseDetail_url,json=data)
        res = res.json()
        status = res["code"]
        assert "2000000" == status, "下发补充材料失败，status不为2000000"  # 断言使用Python原生assert
        assert "操作成功" == res['msg']