-- 本日内贸进场情况
select
	IFNULL(SUM(case when goa.goa_opproc = '014' then goa.goa_gtpks else 0 end),0) as 件数,
	IFNULL(SUM(case when goa.goa_opproc = '014' then goa.goa_gtwg else 0 end),0) as 重量
from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
join ODS_BLJ_WMS_YARD_GOODS_DF wyg on goa.goa_wyg_id = wyg.wyg_id
join ODS_BLJ_BPS_VOYAGE_DF voy on wyg.wyg_ivoy_id = voy.voy_id
join ODS_BLJ_PUB_CARGO_KIND_DF pck on wyg.wyg_gtypecd = pck.pck_kind_code
where (pck.pck_kind_code = '041' or pck.pck_parent_id = '041') and voy.voy_trade = 'N'
    and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d') = '{workdate}'
;