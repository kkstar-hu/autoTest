import json
import os
import re

import pytest
from Base.basepage import BasePage
from Base.baseinterface import RequestHandler
from Commons.jsonread import read_json
from Commons.yamlread import read_yaml
from GTOSXM.Config import configinterface, config

class Interface(BasePage):
    """
    接口
    """

    def interface_login(self):
        """登录接口获取token"""
        self.logger.info('获取Token')
        req = RequestHandler()
        login_res = req.visit("post", url=configinterface.url, json=configinterface.BodyXRCT)
        login_text = login_res.json()
        assert login_text['result'] == 0
        a = login_text['data']['Token']
        Authorization = 'Bearer '+a
        configinterface.head['Authorization'] = a
        # print(Authorization)

    # @pytest.mark.skipif
    def Intelligent_crossing(self):
        """
        智能道口
        """
        t = 0
        while t <= 2:
            self.logger.info('发送智能道口')
            req = RequestHandler()
            cross = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['智能道口url'],
                                data=json.dumps(read_json(os.path.join(os.getcwd(),'Intelligent_crossing.json'))),
                                headers= configinterface.head)
            assert cross.json()['result'] == 0
            if cross.json()['data']['Msg'] != 0:
                configinterface.boxNumber = cross.json()['data']['OutConNo1']
                configinterface.boxPosition = cross.json()['data']['OutLocation1']
                self.logger.info(f'箱号：{configinterface.boxNumber}')
                self.logger.info(f'场位置: {configinterface.boxPosition}')
                t += 3
            else:
                self.logger.info('智能道口存在延迟，再次请求')
                t += 1




    @pytest.mark.skipif
    def RPSLogin(self):
        """
        RPS登录
        """
        self.logger.info('RPS登录')
        req = RequestHandler()
        rpslogin = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['RPS登录url'],
                             data=json.dumps(read_json(os.path.join(os.getcwd(),'RPSLogin.json'))),
                             headers=configinterface.head)
        a = rpslogin.json()['message'].encode().replace(b'\x05',b'\n').replace(b'\x06',b'\t')
        b = list(a.decode().split('\t'))
        assert rpslogin.json()['result'] == 0
        return re.search(r'\d+$', b[b.index(configinterface.boxNumber)-5]).group() #提取ID中纯数字

    # @pytest.mark.skipif
    def RPSAreaBayList(self):
        """
        RPS倍位列表
        """
        self.logger.info('RPS获取内容，修改TaskID，倍位')
        ad = self.RPSLogin()
        with open((os.path.join(os.getcwd(),'RPSAreaBayList.json')),'rb') as f :
            file_f = json.load(f)
            file_f['TaskID'] = ad  #修改对应TaskID
            with open((os.path.join(os.getcwd(),'RPSAreaBayList.json')),'w') as s :
                json.dump(file_f, s)
        req = RequestHandler()
        rpslist = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['RPS倍位列表url'],
                            data=json.dumps(read_json(os.path.join(os.getcwd(),'RPSAreaBayList.json'))),
                            headers= configinterface.head)
        a = rpslist.json()['message'].encode().replace(b'\x05',b'\n').replace(b'\x06',b'\t')
        b = list(a.decode().split('\t'))
        with open((os.path.join(os.getcwd(),'RPSBayInfo.json')),'rb') as n :
            file_n = json.load(n)
            file_n['TaskId'] = ad  # 修改对应TaskID
            file_n['BayNo'] = b[0] # 修改倍位
            with open((os.path.join(os.getcwd(),'RPSBayInfo.json')),'w') as m :
                json.dump(file_n,m)
        with open((os.path.join(os.getcwd(),'RPSSend.json')), 'rb') as p :
            file_p = json.load(p)
            file_p['TaskId'] = ad
            with open((os.path.join(os.getcwd(), 'RPSSend.json')), 'w') as q:
                json.dump(file_p, q)


    # @pytest.mark.skipif
    def RPSBayInfo(self):
        """
        RPS倍位结构
        """
        self.logger.info('RPS获取内容，修改CntrId，Ylocation')
        req = RequestHandler()
        rpsbody = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['RPS倍位结构url'],
                            data=json.dumps(read_json(os.path.join(os.getcwd(),'RPSBayInfo.json'))),
                            headers= configinterface.head)
        a = rpsbody.json()['message'].encode().replace(b'\x05',b'\n').replace(b'\x06',b'\t')
        b = list(a.decode().split('\t'))
        with open((os.path.join(os.getcwd(),'RPSSend.json')), 'rb') as p :
            file_p = json.load(p)
            file_p['CntrId'] = b[2]
            file_p['Ylocation'] = configinterface.boxPosition
            with open((os.path.join(os.getcwd(), 'RPSSend.json')), 'w') as q:
                json.dump(file_p, q)

    # @pytest.mark.skipif
    def RPSSend(self):
        """
        RPS发箱确认
        """
        self.logger.info('RPS发箱')
        req = RequestHandler()
        rpssend = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['RPS确认url'],
                            data=json.dumps(read_json(os.path.join(os.getcwd(),'RPSSend.json'))),
                            headers= configinterface.head)
        self.logger.info(rpssend.json())


    @pytest.mark.skipif
    def RPSareaNO(self):
        """
        RPS倍位
        """
        req = RequestHandler()
        rpsareano = req.visit('post', url=read_yaml(os.path.join('interface.yaml'))[0]['RPS倍位url'],
                             data=json.dumps(read_json(os.path.join(os.getcwd(), 'RPSareaNO.json'))),
                             headers= configinterface.head)
        a = rpsareano.json()['message'].encode().replace(b'\x05',b'\n').replace(b'\x06',b'\t')
        print(a)
        b = list(a.decode().split('\t'))
        print(b)


