import json
import os

import pytest
from Base.basepage import BasePage
from Commons.interface_request import RequestHandler
from Commons.operateJson import read_json
from Commons.yamlread import read_yaml
from GTOSXM.Config import configinterface, config

shipid = {
    "iVoyId": 6294
}
Authorization = 'Bearer '


class Interface_Page(BasePage):
    """
    大船接口
    """

    def interface_login(self):
        """登录接口获取token"""
        req = RequestHandler()
        login_res = req.visit("post", url=configinterface.loginurl, json=configinterface.BodyXRCT)
        login_text = login_res.json()
        assert login_text['result'] == 0
        a = login_text['data']['Token']
        Authorization = 'Bearer ' + a
        configinterface.head['Authorization'] = a
        print(Authorization)

    @pytest.mark.skipif
    def interface_cangdan(self):
        """创建舱单"""
        req = RequestHandler()
        cangdan = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['舱单url'],
                            data=json.dumps(read_json(os.path.join(os.getcwd(), 'json', 'cangdan.json'))),
                            headers=configinterface.head)
        assert cangdan.json()['result'] == 0

    @pytest.mark.skipif
    def interface_cangdanxiang(self):
        """创建舱单箱"""
        req = RequestHandler()
        cangdanbox = req.visit('post', url=read_yaml(os.path.join('../Interface_Test/interface.yaml'))[0]['舱单url'],
                               data=json.dumps(
                                   read_json(os.path.join(os.getcwd(), 'json', 'cangdanxiang.json'))),
                               headers=configinterface.head)
        print(cangdanbox.json())

    @pytest.mark.skipif
    def interface_fangxiang(self):
        """舱单发箱"""
        req = RequestHandler()
        faxiang = req.visit('post',
                            url=read_yaml(os.path.join(os.getcwd(), '../Interface_Test/interface.yaml'))[0]['发箱url'],
                            json=shipid,
                            headers=configinterface.head)

        assert faxiang.json()['result'] == 0


    def interface_getboxno(self, boxnumber):
        """查箱id"""
        box_id_json = {"commonSearch": {"QueryType": ["IYC"], "CtnNos": [f"{boxnumber}"], "Termcode": ["XRCT"]}}
        req = RequestHandler()
        response = req.visit('post', url=configinterface.url+"/api/generic/portal?nameSpace=SHB.Cloud.TOS.DMS.Contract.Query&className=IQuery&methodName=QueryCtnInOutHistories",
                              json=box_id_json, headers=configinterface.head)
        # print(response.json())
        boxid=response.json()['data'][0]['ContainerID']
        voyid=response.json()['data'][0]['ExportVoyageID']
        return boxid, voyid

    # @pytest.mark.skipif
    def interface_getsendboxno(self, boxnumber):
        """查发箱id"""
        k = []
        req = RequestHandler()
        self.ShipID(boxnumber)
        self.interface_getboxno(boxnumber)
        sendbox = req.visit('post',
                            url=read_yaml(os.path.join(os.getcwd(), '../Interface_Test/interface.yaml'))[0]['监控url'],
                            data=json.dumps(read_json(
                                os.path.join(os.getcwd(), 'json', 'zhuangchuanfaxiang.json'))),
                            headers=configinterface.head)
        print(sendbox.json()['data'])
        for i in sendbox.json()['data']:
            print(i['CntrAuditList'])
            for j in i['CntrAuditList']:
                k.append(j)
        with open((os.path.join(os.getcwd(), 'json', 'zuoyefaxiang.json')), 'rb') as f:
            file_f = json.load(f)
            file_f['vpcIds'] = [k[0]['ContainerID']]
            with open((os.path.join(os.getcwd(), 'json', 'zuoyefaxiang.json')), 'w') as s:
                json.dump(file_f, s)
        with open((os.path.join(os.getcwd(), 'json', 'yunxuzhiti.json')), 'rb') as q:
            file_q = json.load(q)
            file_q['vpcIds'] = [k[0]['ContainerID']]
            with open((os.path.join(os.getcwd(), 'json', 'yunxuzhiti.json')), 'w') as p:
                json.dump(file_q, p)

    # @pytest.mark.skipif
    def ShipID(self, boxnumber):
        """查计划ID，航次ID"""
        shipname = ''
        req = RequestHandler()
        with open((os.path.join(os.getcwd(), 'json', 'boxID.json')), 'rb') as a:
            file_a = json.load(a)
            file_a['commonSearch']['CtnNos'] = [f'{boxnumber}']
            with open((os.path.join(os.getcwd(), 'json', 'boxID.json')), 'w') as b:
                json.dump(file_a, b)
            boxid = req.visit('post',
                              url=read_yaml(os.path.join(os.getcwd(), '../Interface_Test/interface.yaml'))[0][
                                  '箱号url'],
                              data=json.dumps(
                                  read_json(os.path.join(os.getcwd(), 'json', 'boxID.json'))),
                              headers=configinterface.head)
            for i in boxid.json()['data']:
                if boxnumber == config.boxNumber:
                    for j in i['InGoodsBillInfos']:
                        # 全称
                        shipname = i['ImportVesselName'][:2] + '/' + i['ImportVesselName'][2:] + i['ImportVesselName'][
                                                                                                 2:] + '/' + i[
                                       'ImportVoyage'] + '/' + i['ImportVoyage'][:1]
                        with open((os.path.join(os.getcwd(), 'json', 'chuanqi.json')), 'rb') as f:
                            file_f = json.load(f)
                            for k in file_f['dynamicConditions']:
                                for q in k['conditionValues']:
                                    q['displayName'] = shipname
                                    # 航次名称
                                    q['value'] = j['VoyageID']
                                    with open((os.path.join(os.getcwd(), 'json', 'chuanqi.json')),
                                              'w') as c:
                                        json.dump(file_f, c)
                if boxnumber == config.outBoxNumber:
                    for j in i['OutBillGoodsInfos']:
                        with open((os.path.join(os.getcwd(), 'json', 'peizai.json')), 'rb') as d:
                            file_d = json.load(d)
                            file_d['VoyID'] = j['VoyageID']
                            for L in file_d['StowageLocs']:
                                L['VoyID'] = j['VoyageID']
                                with open((os.path.join(os.getcwd(), 'json', 'peizai.json')),
                                          'w') as e:
                                    json.dump(file_d, e)

    # @pytest.mark.skipif
    def modify_position(self, number):
        """
        修改船箱位
        """
        with open((os.path.join(os.getcwd(),'../Interface_Test', 'json', 'peizai.json')), 'rb') as f:
            file_f = json.load(f)
            for i in file_f['StowageLocs']:
                i['VLocation'] = number
                with open((os.path.join(os.getcwd(), '../Interface_Test', 'json', 'peizai.json')), 'w') as s:
                    json.dump(file_f, s)
