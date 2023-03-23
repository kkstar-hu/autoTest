import json
import os

import pytest

from Base.baseinterface import RequestHandler
from Commons.jsonread import read_json
from Commons.yamlread import read_yaml
from GTOSXM.Config import configinterface, config

shipid = {
	"iVoyId": 6294
}
Authorization = 'Bearer '

def testinterface_login():
    """登录接口获取token"""
    req = RequestHandler()
    login_res = req.visit("post", url=configinterface.url, json=configinterface.BodyXRCT)
    login_text = login_res.json()
    # print(login_text)
    assert login_text['result'] == 0
    a = login_text['data']['Token']
    Authorization = 'Bearer '+a
    configinterface.head['Authorization'] = a
    print(Authorization)


@pytest.mark.skipif
def testinterface_cangdan():
    """创建舱单"""
    req = RequestHandler()
    cangdan = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['舱单url'],
                        data=json.dumps(read_json(os.path.join(os.getcwd(),'JSOn','cangdan.json'))),
                        headers= configinterface.head)
    # print(cangdan)
    assert cangdan.json()['result'] == 0
    # print(cangdan.json())

@pytest.mark.skipif
def testinterface_cangdanxiang():
    """创建舱单箱"""
    req = RequestHandler()
    cangdanbox = req.visit('post', url=read_yaml(os.path.join('../Interface_Test/interface.yaml'))[0]['舱单url'],
                        data=json.dumps(read_json(os.path.join(os.getcwd(),'../Interface_Test/JSOn','cangdanxiang.json'))),
                        headers= configinterface.head)
    print(cangdanbox.json())

@pytest.mark.skipif
def testinterface_fangxiang():
    """舱单发箱"""
    req = RequestHandler()
    faxiang = req.visit('post',url=read_yaml(os.path.join(os.getcwd(),'../Interface_Test/interface.yaml'))[0]['发箱url'],
                        json=shipid,
                        headers= configinterface.head)

    assert faxiang.json()['result'] == 0
    # print(faxiang.json())

# @pytest.mark.skipif
def testinterface_getboxno(boxnumber):
    """查箱id"""
    req = RequestHandler()
    with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\boxID.json','rb') as a:
        file_a = json.load(a)
        # print(file_a['commonSearch']['CtnNos'])
        file_a['commonSearch']['CtnNos'] = [f'{boxnumber}']
        # print(file_a)
        with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\boxID.json','w') as b:
            json.dump(file_a,b)
    boxid = req.visit('post',url=read_yaml(os.path.join(os.getcwd(),'../Interface_Test/interface.yaml'))[0]['箱号url'],
                      data=json.dumps(read_json(os.path.join(os.getcwd(),'../Interface_Test/JSOn','boxID.json'))),
                      headers=configinterface.head)
    # print(boxid.json()['data'])
    for i in boxid.json()['data']:
        with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\peizai.json','rb') as f:
            file = json.load(f)
            # print(file)
            for j in file['StowageContainers']:
                j['ContainerID'] = i['ContainerID']
                # print(file)
                with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\peizai.json','w') as r:
                    json.dump(file,r)
        with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\zhuangchuanfaxiang.json','rb') as zf:
            file_zf = json.load(zf)
            # print(file_zf)
            file_zf['cntrID'] = i['ContainerID']
            # print(file_zf)
            with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\zhuangchuanfaxiang.json', 'w') as zr:
                json.dump(file_zf, zr)
    testShipID(boxnumber)

# @pytest.mark.skipif
def testinterface_getsendboxno(boxnumber):
    """查发箱id"""
    k = []
    req = RequestHandler()
    testShipID(boxnumber)
    testinterface_getboxno(boxnumber)
    sendbox = req.visit('post',url = read_yaml(os.path.join(os.getcwd(),'../Interface_Test/interface.yaml'))[0]['监控url'],
                        data = json.dumps(read_json(os.path.join(os.getcwd(),'../Interface_Test/JSOn','zhuangchuanfaxiang.json'))),
                        headers = configinterface.head)
    print(sendbox.json()['data'])
    # for i in sendbox.json()['data']:
    #     print(i['CntrAuditList'])
    #     for j in i['CntrAuditList']:
    #         k.append(j)
    # # print(k[0]['ContainerID'])
    # with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\zuoyefaxiang.json','rb') as f:
    #     file_f = json.load(f)
    #     # print(file_f)
    #     file_f['vpcIds'] = [k[0]['ContainerID']]
    #     # print(file_f)
    #     with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\zuoyefaxiang.json','w') as s:
    #         json.dump(file_f,s)
    # with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\yunxuzhiti.json','rb') as q:
    #     file_q = json.load(q)
    #     # print(file_q)
    #     file_q['vpcIds'] = [k[0]['ContainerID']]
    #     # print(file_q)
    #     with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\yunxuzhiti.json','w') as p:
    #         json.dump(file_q,p)


# @pytest.mark.skipif
def testShipID(boxnumber):
    """查计划ID，航次ID"""
    shipname =''
    req = RequestHandler()
    with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\boxID.json','rb') as a:
        file_a = json.load(a)
        # print(file_a['commonSearch']['CtnNos'])
        file_a['commonSearch']['CtnNos'] = [f'{boxnumber}']
        # print(file_a)
        with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\boxID.json','w') as b:
            json.dump(file_a,b)
        boxid = req.visit('post',
                          url=read_yaml(os.path.join(os.getcwd(),'../Interface_Test/interface.yaml'))[0]['箱号url'],
                          data=json.dumps(read_json(os.path.join(os.getcwd(),'../Interface_Test/JSOn','boxID.json'))),
                          headers=configinterface.head)
        # print(boxid.json()['data'])
        for i in boxid.json()['data']:
            if boxnumber == config.boxNumber:
            # 航次名称
            #     print(i['ImportVoyage'])
                for j in i['InGoodsBillInfos']:
                    # print(j['VoyageID'])
                    #全称
                    shipname = i['ImportVesselName'][:2]+'/'+i['ImportVesselName'][2:]+i['ImportVesselName'][2:]+'/'+i['ImportVoyage']+'/'+i['ImportVoyage'][:1]
                    # print(shipname)
                    with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\chuanqi.json','rb') as f:
                        file_f = json.load(f)
                        # print(file_f['dynamicConditions'])
                        for k in file_f['dynamicConditions']:
                            # print(k['conditionValues'])
                            for q in k['conditionValues']:
                                # print(q['displayName'])
                                # print(q['value'])
                                q['displayName'] = shipname
                                q['value'] = j['VoyageID']
                                with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\chuanqi.json','w') as c:
                                    json.dump(file_f,c)
            if boxnumber == config.outBoxNumber:
                # print(i)
                for j in i['OutBillGoodsInfos']:
                    # print(j['VoyageID'])
                    with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\peizai.json','rb') as d:
                        file_d = json.load(d)
                        # print(file_d)
                        # print(file_d['VoyID'])
                        file_d['VoyID'] = j['VoyageID']
                        # print(file_d)
                        # print(file_d['StowageLocs'])
                        for L in file_d['StowageLocs']:
                            L['VoyID'] = j['VoyageID']
                            # print(file_d)
                            with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\peizai.json','w') as e:
                                json.dump(file_d,e)

# @pytest.mark.skipif
def testmodify_position(numbers):
    """
    修改船箱位
    """
    with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\peizai.json','rb') as f :
        file_f = json.load(f)
        # print(file_f['StowageLocs'])
        for i in file_f['StowageLocs']:
            # print(i['VLocation'])
            i['VLocation'] = numbers
            # print(file_f)
            with open(r'D:\ATA\autoTest\GTOSXM\TestCase\Interface_Test\JSOn\peizai.json','w') as s :
                json.dump(file_f, s)

