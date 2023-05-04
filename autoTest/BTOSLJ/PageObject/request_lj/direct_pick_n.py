# -*- coding:utf-8 -*-
from BTOSLJ.Controls.BTOS_requests import RequestMain
import pytest_check as check


class DirectPickN(RequestMain):

    def test_add_outdoor_record(self, schema=None):
        pass


    def test_search_outdoor_record(self, schema=None, otr_truckno="", otr_outdrno="", odr_invno=""):
        """
        :param schema:
        :param otr_truckno: 车牌号
        :param otr_outdrno: 出门证编号
        :param odr_invno: 运输公司ID
        :return:
        """

        params = {
            "total": 0,
            "current": 1,
            "size": 20,
            "otrTruckno": otr_truckno,
            "otrOutdrNo": otr_outdrno,
            "odrInvNo": odr_invno,
            "orderItems": "createTime DESC"
        }
        res = self.request_main("get", "/tos/gts/outdoorRecord/direct/page", params=params)
        data = res.json()
        check.equal(data["status"], "200")
        # check.equal(self.check_json(data, schema), True)
        self.logger.info("GET /tos/gts/outdoorRecord/direct/page\n参数: {}\n".format(params) + str(self.format(data)))


if __name__ == '__main__':
    _a = DirectPickN("10.166.0.131:20000")
    _a.test_search_outdoor_record()