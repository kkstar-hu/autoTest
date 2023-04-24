-- 船代外贸进出口
with res as(
	select goa_opdate ,scd.scd_ivoyage as 航次, voy_id, cst.cst_shrtnm as 船代, voy.voy_iefg, goa_gtwg/10000 as 吨位,
	(case when goa_gtwg > goa_gtvol then goa_gtwg else goa_gtvol end)/10000 as 计费吨
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join ODS_BLJ_BPS_VOYAGE_DF voy on goa.goa_voy_id = voy.voy_id
	join ODS_BLJ_BPS_SCHEDULE_DF scd on voy.voy_scd_id = scd.scd_id
	join ODS_BLJ_PUB_CUSTOMERS_DF cst on scd.scd_ivagt = cst.cst_cstmcd and scd.tenant_id = cst.tenant_id
	where voy.voy_iefg = 'I' and voy.voy_trade = 'W'
	union all
	select goa_opdate, scd.scd_evoyage as 航次 ,voy_id, cst.cst_shrtnm as 船代, voy.voy_iefg, goa_gtwg/10000 as 吨位,
	(case when goa_gtwg > goa_gtvol then goa_gtwg else goa_gtvol end)/10000 as 计费吨
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join ODS_BLJ_BPS_VOYAGE_DF voy on goa.goa_voy_id = voy.voy_id
	join ODS_BLJ_BPS_SCHEDULE_DF scd on voy.voy_scd_id = scd.scd_id
	join ODS_BLJ_PUB_CUSTOMERS_DF cst on scd.scd_evagt = cst.cst_cstmcd and scd.tenant_id = cst.tenant_id
	where voy.voy_iefg = 'E' and voy.voy_trade = 'W'
)
select DATE_FORMAT(res.goa_opdate ,'%Y-%m') as 月份, res.船代,
	COUNT(distinct case when res.voy_iefg='I' then res.voy_id else null end) as 外贸进口艘次,
	SUM(case when res.voy_iefg='I' then res.吨位 else 0 end) as 外贸进口吨位,
	SUM(case when res.voy_iefg='I' then res.计费吨 else 0 end) as 外贸进口计费吨,
	COUNT(distinct case when res.voy_iefg='E' then res.voy_id else null end) as 外贸出口艘次,
	SUM(case when res.voy_iefg='E' then res.吨位 else 0 end) as 外贸出口吨位,
	SUM(case when res.voy_iefg='E' then res.计费吨 else 0 end) as 外贸出口计费吨,
	COUNT(distinct case when res.voy_id is not null then res.voy_id else null end) as 合计艘次,
	SUM(res.吨位) as 合计吨位, SUM(res.计费吨) as 合计计费吨,
	ye.年度合计艘次, ye.年度合计吨位, ye.年度合计计费吨
from res
left join (
		select DATE_FORMAT(res.goa_opdate ,'%Y') as 年份, res.船代,
			COUNT(distinct case when res.voy_id is not null then res.voy_id else null end) as 年度合计艘次,
			SUM(res.吨位) as 年度合计吨位, SUM(res.计费吨) as 年度合计计费吨
		from res
		group by DATE_FORMAT(res.goa_opdate ,'%Y'),res.船代
	 ) ye
	 on DATE_FORMAT(res.goa_opdate ,'%Y') = ye.年份 and res.船代 = ye.船代
where DATE_FORMAT(res.goa_opdate ,'%Y-%m') = '{workdate}'
group by DATE_FORMAT(res.goa_opdate ,'%Y-%m') ,res.船代, ye.年度合计艘次, ye.年度合计吨位, ye.年度合计计费吨
order by 合计艘次 desc
;