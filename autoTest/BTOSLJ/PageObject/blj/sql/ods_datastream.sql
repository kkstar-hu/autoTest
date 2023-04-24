-- ����ͬ��
-- ���ػ���̬
truncate table ODS.ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI;
insert into ODS.ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI
SELECT goa_id, goa_opdate, goa_dst_id, goa_shift_no, goa_optype, goa_opproc, goa_wyg_id, goa_ygo_id,
goa_ygt_id, goa_handset, goa_gtwg, goa_gtpks, goa_gtvol, goa_ymc_id, goa_voy_id, goa_gat_id, goa_whwl_id,
goa_wver_id, goa_glength, goa_gwidth, goa_gheight, goa_dynamicloc, goa_direction, goa_planno, goa_large_sized,
goa_danger, goa_cover, goa_piece_no, goa_cntr_no, goa_contract_no, goa_specs, goa_damage, goa_carrier_type,
goa_carrier_name, goa_hatch_no, goa_leader_conf, goa_tally_conf, goa_ref_id, goa_termcd, goa_inyard_date,
tenant_id, data_version, create_user, create_time, update_user, update_time, goa_tally_id, goa_bag_id, goa_direct,
goa_iofg, goa_remark, goa_real_shift, goa_share_flag, goa_aduit_flag, goa_piece_code, goa_plg_id, goa_damage_remark,
goa_sheet_no
FROM JDBC_PG_BLJ.btops.wms_goods_occupy_activities;
-- ���ػ���ϸ
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_DTL_DI;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_DTL_DI
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods_dtl;
-- ���ػ�
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_DF;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods;
-- ���ػ�ռλ
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods_occupy;
-- ���ػ����
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_REVIEW_DF;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_REVIEW_DF
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods_review;
-- �յ�
truncate table ODS.ODS_BLJ_BUS_BILLS_DF;
insert into ODS.ODS_BLJ_BUS_BILLS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bus_bills;
-- �յ���
truncate table ODS.ODS_BLJ_BUS_GOODS_DF;
insert into ODS.ODS_BLJ_BUS_GOODS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bus_goods;
-- �����
truncate table ODS.ODS_BLJ_PAS_PLAN_GOODS_DF;
insert into ODS.ODS_BLJ_PAS_PLAN_GOODS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pas_plan_goods;
-- ��ҵƱ
truncate table ODS.ODS_BLJ_PWS_WORK_SHEET_DF;
insert into ODS.ODS_BLJ_PWS_WORK_SHEET_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_work_sheet;
-- װж����ҵƱ
truncate table ODS.ODS_BLJ_PWS_WORK_SHEET_WK_DF;
insert into ODS.ODS_BLJ_PWS_WORK_SHEET_WK_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_work_sheet_wk;
-- Ա����ҵƱ
truncate table ODS.ODS_BLJ_PWS_WORK_SHEET_MACHINE_DF;
insert into ODS.ODS_BLJ_PWS_WORK_SHEET_MACHINE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_work_sheet_machine;
-- ��ҵƱ����
truncate table ODS.ODS_BLJ_PWS_QUOTA_DF;
insert into ODS.ODS_BLJ_PWS_QUOTA_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_quota;
-- ��˰
truncate table ODS.ODS_BLJ_BUS_BILL_BONDED_DF;
insert into ODS.ODS_BLJ_BUS_BILL_BONDED_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bus_bill_bonded;
-- �����ȼ�
truncate table ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_ITEM_DF;
insert into ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_ITEM_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_weight_level_item;
-- ��������
truncate table ODS.ODS_BLJ_BPS_VESSELS_DF;
insert into ODS.ODS_BLJ_BPS_VESSELS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_vessels;
-- ����
truncate table ODS.ODS_BLJ_BPS_SCHEDULE_DF;
insert into ODS.ODS_BLJ_BPS_SCHEDULE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_schedule;
-- ����
truncate table ODS.ODS_BLJ_BPS_VOYAGE_DF;
insert into ODS.ODS_BLJ_BPS_VOYAGE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_voyage;
-- ����
truncate table ODS.ODS_BLJ_BPS_VESSEL_BERTHES_DF;
insert into ODS.ODS_BLJ_BPS_VESSEL_BERTHES_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_vessel_berthes;
-- �ͻ�����
truncate table ODS.ODS_BLJ_PUB_CUSTOMERS_DF;
insert into ODS.ODS_BLJ_PUB_CUSTOMERS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_customers;
-- �ͻ�����
truncate table ODS.ODS_BLJ_PUB_CUSTOMERS_ROLE_DF;
insert into ODS.ODS_BLJ_PUB_CUSTOMERS_ROLE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_customers_role;
-- ��������
truncate table ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_DF;
insert into ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_weight_level;
