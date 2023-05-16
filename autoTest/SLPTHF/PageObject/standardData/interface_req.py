from SLPTHF.Controls.SLPT_requests import RequestMain
from Commons.operateJson import operateJson
import pytest_check as check

class InterfaceReq(RequestMain):
    def req_add_ship_spec(self,schema):
        Authorization = self.get_token()
        headers = {
              'Authorization': 'Bearer '+Authorization,
              'Content-Type': 'application/json'
            }
        res = self.request_main("post", schema['url'],headers=headers, data=schema['request'])
        data = res.json()
        status = operateJson().find_values(data, 'status')
        check.equal(res.status_code, 200)
        check.equal(status, 200)
        self.logger.info("新增船舶(/api/v1/std/vessels)-接口返回值\n参数: {}\n".format(schema['request']) + str(self.format(data)))

if __name__ == '__main__':
    schema = {'url': '/api/v1/std/vessels', 'request': '{"cd": "AUTOTEST01", "vtpcode": "FCS", "cnname": "自动化测试船舶", "enname": "autotestship01", "callsign": "3U8633", "cstShippingline": "TEST1", "cstAgency": "YCJZ001", "ctyCd": "CN", "loa": "200", "breadth": "0", "gton": "500000", "nettom": "205000", "totallocation": "2000", "baynum": "10", "draftunload": "100", "draftload": "500", "deckmaxtiers": "8", "deckmaxrows": "20", "hatchmaxtiers": "3", "hatchmaxrows": "10", "hatchamount": "8", "hatchcoveramount": "66", "derrickamount": "5", "rfsocket": "50", "stowagereq": "这里是配载要求", "loaddisargereq": "这里是装载要求", "callid": "80069", "pilotage": "N", "stopsign": "N", "publicsign": "N", "uncode": "AUTO01", "actVtpcode": null, "imono": "20230515"}'}
    i=InterfaceReq('10.166.0.162:9088')
    i.req_add_ship_spec(schema)