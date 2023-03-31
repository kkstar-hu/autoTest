# -*- coding:utf-8 -*-
import time
from BTOSLJ.Controls.BTOS_db import GetPg
import uuid
from pandas import DataFrame

class Test(GetPg):

    def select_nowstore(self):
        nowstore_sql = """--分货类今日结存
                with nowstore as(
                    with res as(
                    select wyg.wyg_gtypecd as 货类代码, SUM(ygt.ygt_gtpks) as gtpks, SUM(ygt.ygt_gtwg) as gtwg, SUM(ygt.ygt_gtvol) as gtvol
                    from wms_yard_goods_dtl ygt
                    left join wms_yard_goods wyg on wyg.wyg_id = ygt_wyg_id
                    group by wyg.wyg_gtypecd
                    )
                    select 
                    (CASE WHEN pck.pck_stat_code IS NOT NULL THEN 
                        (select pck2.pck_kind_name from pub_cargo_kind pck2 where pck2.pck_kind_code = pck.pck_stat_code) 
                        ELSE pck.pck_kind_name END ) as 大货类,
                    sum(res.gtpks) as 库场件数, sum(res.gtwg) as 库场重量, sum(res.gtvol) as 库场体积
                    from res
                    left join pub_cargo_kind pck on res.货类代码 = pck.pck_kind_code
                    group by 
                    (CASE WHEN pck.pck_stat_code IS NOT NULL THEN 
                        (select pck2.pck_kind_name from pub_cargo_kind pck2 where pck2.pck_kind_code = pck.pck_stat_code) 
                        ELSE pck.pck_kind_name END )
                )
                select * from nowstore;
            """

        self.execute_sql(nowstore_sql)
        df = self.cur.fetchall()
        self.logger.info("分货类库场数量\n%s", DataFrame(df))

    def insert_goa_dc(self):
        goa_id = uuid.uuid1().hex
        date = time.strftime("%Y-%m-%d 00:00:00.000", time.localtime())
        # goa_iofg 货物进出标记，0进出，1进，2出
        # goa_direct 是否直装直提
        insert_goa_dc_sql = """
            INSERT INTO btops.wms_goods_occupy_activities 
            (goa_id,goa_opdate,goa_dst_id,goa_shift_no,goa_optype,goa_opproc,goa_wyg_id,goa_ygo_id,goa_ygt_id,goa_handset,goa_gtwg,goa_gtpks,goa_gtvol,goa_ymc_id,goa_voy_id,goa_gat_id,goa_whwl_id,goa_wver_id,goa_glength,goa_gwidth,goa_gheight,goa_dynamicloc,goa_direction,goa_planno,goa_large_sized,goa_danger,goa_cover,goa_piece_no,goa_cntr_no,goa_contract_no,goa_specs,goa_damage,goa_carrier_type,goa_carrier_name,goa_hatch_no,goa_leader_conf,goa_tally_conf,goa_ref_id,goa_termcd,goa_inyard_date,tenant_id,data_version,create_user,create_time,update_user,update_time,goa_tally_id,goa_bag_id,goa_direct,goa_iofg,goa_remark,goa_real_shift,goa_share_flag,goa_aduit_flag,goa_piece_code,goa_plg_id,goa_damage_remark,goa_sheet_no,goa_reflector,goa_harbor) 
            VALUES
            ('{uid}','{date1}','8d5f6e9786b25fb97e976e9ce56173a4','1','DC','009','f787296222d1be6a3e7e9419cc8ea945','6cde83376e4e231dfc1b70613ffe07bc','92b71d92b1881362a2c7046687fa5673',NULL,500.000,20,100.000,NULL,'6379eab39ea93daeae49d4e5f9b968e7','c1dd94241e837fbebfdb15174b6371c5',NULL,NULL,0.00,0.00,0.00,'*','*','PK20221213001','N','N','N','*','*','*','*','0','T','津A00001','01','','ab92384629e3baf5f4d318e4d522ec87',NULL,'L','{date2}','SIPGLJ',1,'f962e62d60e643a293eb35103b93cc58','{date3}',NULL,NULL,'1de846b1a6ac4647ae4d0a5fb23c7f5e',NULL,'N',0,'',NULL,'000','N','',NULL,NULL,NULL,'N','N')
            returning *;
        """.format(uid=goa_id, date1=date,date2=date,date3=date)
        self.execute_sql(insert_goa_dc_sql)
        self.logger.info("Insert into wms_goods_occupy_activities success: goa_id = %s", goa_id)
        return goa_id

    def delete_goa(self, goa_id):
        delete_sql = f"""
            delete from
            wms_goods_occupy_activities
            where goa_id = '{goa_id}';
        """
        self.execute_sql(delete_sql)
        self.logger.info("Delete from wms_goods_occupy_activities success: goa_id = %s", goa_id)







if __name__ == "__main__":
    a = Test()
    a.select_nowstore()
    goa_id = a.insert_goa_dc()
    a.delete_goa(goa_id)