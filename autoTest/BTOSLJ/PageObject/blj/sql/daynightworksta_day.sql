-- 昼夜情况表-分货类结存
with nowstore as(
	with res as(
		select IFNULL(pck.pck_stat_code ,pck.pck_kind_code) as 大货类,
			IFNULL(SUM(ygt.ygt_gtpks),0) as gtpks, IFNULL(SUM(ygt.ygt_gtwg),0) as gtwg,
			IFNULL(SUM(ygt.ygt_gtvol),0) as gtvol
		from ODS_BLJ_WMS_YARD_GOODS_DTL_DI ygt
		join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = ygt.ygt_wyg_id
		join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = ygt.ygt_ygo_id
		join ODS_BLJ_PUB_CARGO_KIND_DF pck on wyg.wyg_gtypecd = pck.pck_kind_code
		where ygt.tenant_id = 'SIPGLJ' and wyg.wyg_termcd = 'L' and ygo.ygo_type not in ('DL', 'DU')
		group by IFNULL(pck.pck_stat_code ,pck.pck_kind_code)
	)
	SELECT pck2.pck_kind_name as 大货类, gtpks as 库场件数 ,gtwg as 库场重量 ,gtvol as 库场体积, pck2.pck_kind_code
	from res
	left join ODS_BLJ_PUB_CARGO_KIND_DF pck2 on res.大货类 = pck2.pck_kind_code
),
history as(
	with res as(
		select IFNULL(pck.pck_stat_code ,pck.pck_kind_code) as 大货类,
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtpks else 0 end) as igtpks,
		SUM(case when goa.goa_iofg = '1' then goa.goa_gtwg  else 0 end) as igtwg,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtpks else 0 end) as ogtpks,
		SUM(case when goa.goa_iofg = '2' then goa.goa_gtwg  else 0 end) as ogtwg
		from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
		join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = goa.goa_wyg_id
		join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = goa.goa_ygo_id
		join ODS_BLJ_PUB_CARGO_KIND_DF pck on wyg.wyg_gtypecd = pck.pck_kind_code
		where goa.tenant_id = 'SIPGLJ' and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d')>'{workdate}'
			   and goa_optype in ('LD', 'DC', 'DE', 'PK', 'OI', 'OO') and wyg.wyg_termcd = 'L'
			   and ygo_type not in ('DL', 'DU')
		group by IFNULL(pck.pck_stat_code ,pck.pck_kind_code)
	)
	SELECT pck2.pck_kind_name as 大货类, igtpks ,igtwg ,ogtpks, ogtwg, pck2.pck_kind_code
	from res
	left join ODS_BLJ_PUB_CARGO_KIND_DF pck2 on res.大货类 = pck2.pck_kind_code
)
select pck2.pck_kind_name as 大货类,(IFNULL(nowstore.库场件数,0)-(IFNULL(history.igtpks,0)-IFNULL(history.ogtpks,0))) as 本日结存件数,
	(IFNULL(nowstore.库场重量,0)-(IFNULL(history.igtwg,0)-IFNULL(history.ogtwg,0))) as 本日结存重量
from (select distinct IFNULL(pck_stat_code ,pck_kind_code) as kind_code
		from ODS_BLJ_PUB_CARGO_KIND_DF where tenant_id= 'SIPGLJ') pck
left join ODS_BLJ_PUB_CARGO_KIND_DF pck2 on pck.kind_code = pck2.pck_kind_code
left join nowstore on pck.kind_code = nowstore.pck_kind_code
left join history on pck.kind_code = history.pck_kind_code
where (IFNULL(nowstore.库场件数,0)-(IFNULL(history.igtpks,0)-IFNULL(history.ogtpks,0)))<>0
    or (IFNULL(nowstore.库场重量,0)-(IFNULL(history.igtwg,0)-IFNULL(history.ogtwg,0)))<>0
order by pck.kind_code;