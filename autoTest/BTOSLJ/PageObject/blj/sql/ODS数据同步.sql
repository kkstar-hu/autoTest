-- 数据同步
-- 场地货动态
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
-- 场地货明细
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_DTL_DI;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_DTL_DI
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods_dtl;
-- 场地货
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_DF;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods;
-- 场地货占位
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods_occupy;
-- 场地货审核
truncate table ODS.ODS_BLJ_WMS_YARD_GOODS_REVIEW_DF;
insert into ODS.ODS_BLJ_WMS_YARD_GOODS_REVIEW_DF
SELECT *
FROM JDBC_PG_BLJ.btops.wms_yard_goods_review;
-- 舱单
truncate table ODS.ODS_BLJ_BUS_BILLS_DF;
insert into ODS.ODS_BLJ_BUS_BILLS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bus_bills;
-- 舱单货
truncate table ODS.ODS_BLJ_BUS_GOODS_DF;
insert into ODS.ODS_BLJ_BUS_GOODS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bus_goods;
-- 受理货
truncate table ODS.ODS_BLJ_PAS_PLAN_GOODS_DF;
insert into ODS.ODS_BLJ_PAS_PLAN_GOODS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pas_plan_goods;
-- 作业票
truncate table ODS.ODS_BLJ_PWS_WORK_SHEET_DF;
insert into ODS.ODS_BLJ_PWS_WORK_SHEET_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_work_sheet;
-- 装卸队作业票
truncate table ODS.ODS_BLJ_PWS_WORK_SHEET_WK_DF;
insert into ODS.ODS_BLJ_PWS_WORK_SHEET_WK_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_work_sheet_wk;
-- 员工作业票
truncate table ODS.ODS_BLJ_PWS_WORK_SHEET_MACHINE_DF;
insert into ODS.ODS_BLJ_PWS_WORK_SHEET_MACHINE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_work_sheet_machine;
-- 作业票定额
truncate table ODS.ODS_BLJ_PWS_QUOTA_DF;
insert into ODS.ODS_BLJ_PWS_QUOTA_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pws_quota;
-- 保税
truncate table ODS.ODS_BLJ_BUS_BILL_BONDED_DF;
insert into ODS.ODS_BLJ_BUS_BILL_BONDED_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bus_bill_bonded;
-- 重量等级
truncate table ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_ITEM_DF;
insert into ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_ITEM_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_weight_level_item;
-- 船舶资料
truncate table ODS.ODS_BLJ_BPS_VESSELS_DF;
insert into ODS.ODS_BLJ_BPS_VESSELS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_vessels;
-- 船期
truncate table ODS.ODS_BLJ_BPS_SCHEDULE_DF;
insert into ODS.ODS_BLJ_BPS_SCHEDULE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_schedule;
-- 航次
truncate table ODS.ODS_BLJ_BPS_VOYAGE_DF;
insert into ODS.ODS_BLJ_BPS_VOYAGE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_voyage;
-- 靠泊
truncate table ODS.ODS_BLJ_BPS_VESSEL_BERTHES_DF;
insert into ODS.ODS_BLJ_BPS_VESSEL_BERTHES_DF
SELECT *
FROM JDBC_PG_BLJ.btops.bps_vessel_berthes;
-- 客户资料
truncate table ODS.ODS_BLJ_PUB_CUSTOMERS_DF;
insert into ODS.ODS_BLJ_PUB_CUSTOMERS_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_customers;
-- 客户类型
truncate table ODS.ODS_BLJ_PUB_CUSTOMERS_ROLE_DF;
insert into ODS.ODS_BLJ_PUB_CUSTOMERS_ROLE_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_customers_role;
-- 重量分类
truncate table ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_DF;
insert into ODS.ODS_BLJ_PUB_WEIGHT_LEVEL_DF
SELECT *
FROM JDBC_PG_BLJ.btops.pub_weight_level;
