-- 航线统计表
with toyear as(
	select DATE_FORMAT(goa.goa_opdate ,'%m') as 月份 ,sln.sln_cnname, SUM(goa.goa_gtwg)/10000 as 总量
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join ODS_BLJ_BPS_VOYAGE_DF voy on goa.goa_voy_id = voy.voy_id
	join ODS_BLJ_PUB_SERVICE_LINES_DF sln on voy.voy_sln_id = sln.sln_code
	where goa.goa_optype = 'LD' and voy.voy_trade = 'W' and voy.voy_iefg = 'E'
		and DATE_FORMAT(goa.goa_opdate ,'%Y')='{yyyy1}'
	group by DATE_FORMAT(goa.goa_opdate ,'%m'), sln.sln_cnname
),
yesyear as(
	select DATE_FORMAT(goa.goa_opdate ,'%m') as 月份 ,sln.sln_cnname, SUM(goa.goa_gtwg)/10000 as 总量
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join ODS_BLJ_BPS_VOYAGE_DF voy on goa.goa_voy_id = voy.voy_id
	join ODS_BLJ_PUB_SERVICE_LINES_DF sln on voy.voy_sln_id = sln.sln_code
	where goa.goa_optype = 'LD' and voy.voy_trade = 'W' and voy.voy_iefg = 'E'
		and DATE_FORMAT(goa.goa_opdate ,'%Y')='{yyyy2}'
	group by DATE_FORMAT(goa.goa_opdate ,'%m'), sln.sln_cnname
)
select toyear.月份, toyear.sln_cnname as 航线, toyear.总量, IFNULL(yesyear.总量,0) as 去年同期 ,
	(case when yesyear.总量>0 then (toyear.总量-yesyear.总量)/yesyear.总量 else 0 end) as 同比增减
from toyear
left join yesyear on toyear.月份=yesyear.月份
order by toyear.月份
union all
select toyear.月份, '全部' as 航线, SUM(总量) as 总量 ,0 as 去年同期,0 as 同比增减
from toyear
group by toyear.月份
order by toyear.月份
;