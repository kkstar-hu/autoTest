-- 本日纸浆提货情况
select
	IFNULL(SUM(case when goa.goa_opproc in ('008','0081') then goa.goa_gtpks else 0 end),0) as 车提纸浆件数,
	IFNULL(SUM(case when goa.goa_opproc in ('008','0081') then goa.goa_gtwg else 0 end),0) as 车提纸浆重量,
	IFNULL(SUM(case when goa.goa_opproc in ('011','010') then goa.goa_gtpks else 0 end),0) as 驳提纸浆件数,
	IFNULL(SUM(case when goa.goa_opproc in ('011','010') then goa.goa_gtwg else 0 end),0) as 驳提纸浆重量
from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
join ODS_BLJ_WMS_YARD_GOODS_DF wyg on goa.goa_wyg_id = wyg.wyg_id
where wyg.wyg_gtypecd = '1511' and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d') = '{workdate}'
;