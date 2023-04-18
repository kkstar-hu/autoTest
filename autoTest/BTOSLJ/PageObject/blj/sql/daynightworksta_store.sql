-- 昼夜情况统计表-堆存情况
with nowstore as(
		select
			IFNULL(SUM(ygt.ygt_gtpks),0) as gtpks, IFNULL(SUM(ygt.ygt_gtwg),0) as gtwg,
			IFNULL(SUM(ygt.ygt_gtvol),0) as gtvol, voy.voy_trade
		from ODS_BLJ_WMS_YARD_GOODS_DTL_DI ygt
		join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = ygt.ygt_wyg_id
		join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = ygt.ygt_ygo_id
		join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id, wyg.wyg_evoy_id) = voy.voy_id
		where ygt.tenant_id = 'SIPGLJ' and wyg.wyg_termcd = 'L' and ygo.ygo_type not in ('DL', 'DU')
		group by voy.voy_trade
),
history1 as(
	select
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtpks else 0 end) as igtpks,
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtwg  else 0 end) as igtwg,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtpks else 0 end) as ogtpks,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtwg  else 0 end) as ogtwg,
		voy.voy_trade
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = goa.goa_wyg_id
	join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id, wyg.wyg_evoy_id) = voy.voy_id
	join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = goa.goa_ygo_id
	where goa.tenant_id = 'SIPGLJ' and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d')>'{workdate}'
		and goa_optype in ('LD', 'DC', 'DE', 'PK', 'OI', 'OO') and wyg.wyg_termcd = 'L'
		and ygo_type not in ('DL', 'DU')
	group by voy.voy_trade
),
history2 as(
	select
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtpks else 0 end) as igtpks,
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtwg  else 0 end) as igtwg,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtpks else 0 end) as ogtpks,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtwg  else 0 end) as ogtwg,
		voy.voy_trade
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = goa.goa_wyg_id
	join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id, wyg.wyg_evoy_id) = voy.voy_id
	join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = goa.goa_ygo_id
	where goa.tenant_id = 'SIPGLJ' and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d')>DATE_ADD('{workdate}',INTERVAL -1 DAY)
		and goa_optype in ('LD', 'DC', 'DE', 'PK', 'OI', 'OO') and wyg.wyg_termcd = 'L'
		and ygo_type not in ('DL', 'DU')
	group by voy.voy_trade
),
today as(
	select
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtpks else 0 end) as igtpks,
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtwg  else 0 end) as igtwg,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtpks else 0 end) as ogtpks,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtwg  else 0 end) as ogtwg,
		voy.voy_trade
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = goa.goa_wyg_id
	join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id, wyg.wyg_evoy_id) = voy.voy_id
	join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = goa.goa_ygo_id
	where goa.tenant_id = 'SIPGLJ' and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d')='{workdate}'
		and goa_optype in ('LD', 'DC', 'DE', 'PK', 'OI', 'OO') and wyg.wyg_termcd = 'L'
		and ygo_type not in ('DL', 'DU')
	group by voy.voy_trade
)
select (case when nowstore.voy_trade='W' then '外贸' else '内贸' end) as 贸易类型,
	(IFNULL(nowstore.gtpks,0)-(IFNULL(history2.igtpks,0)-IFNULL(history2.ogtpks,0))) as 上日结存件数,
	(IFNULL(nowstore.gtwg,0)-(IFNULL(history2.igtwg,0)-IFNULL(history2.ogtwg,0))) as 上日结存重量,
	IFNULL(today.igtpks,0) as 本日进件数, IFNULL(today.igtwg,0) as 本日进重量,
	IFNULL(today.ogtpks,0) as 本日出件数, IFNULL(today.ogtwg,0) as 本日出重量,
	(IFNULL(nowstore.gtpks,0)-(IFNULL(history1.igtpks,0)-IFNULL(history1.ogtpks,0))) as 本日结存件数,
	(IFNULL(nowstore.gtwg,0)-(IFNULL(history1.igtwg,0)-IFNULL(history1.ogtwg,0))) as 本日结存重量
from nowstore
left join history1 on nowstore.voy_trade = history1.voy_trade
left join history2 on nowstore.voy_trade = history2.voy_trade
left join today on nowstore.voy_trade = today.voy_trade
;