-- 分货类月报
with finaldata as(
	with nowstore as(
		with cname as(
			with res as(
				select wyg.wyg_gtypecd as 货类代码, ybk.ybk_name as 场地区域, SUM(ygt.ygt_gtpks) as gtpks, SUM(ygt.ygt_gtwg) as gtwg, SUM(ygt.ygt_gtvol) as gtvol,
					voy.voy_trade as trade_type
				from ODS_BLJ_WMS_YARD_GOODS_DTL_DI ygt
				left join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = ygt.ygt_wyg_id
				left join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id, wyg.wyg_evoy_id) = voy.voy_id
				left join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = ygt.ygt_ygo_id
				left join ODS_BLJ_PUB_YARD_GOODS_LOCATION_DF ygc on ygo.ygo_ygc_id = ygc.ygc_id
				left join ODS_BLJ_PUB_YARD_BASE_BLOCK_DF ybk on ygc.ygc_ybk_id = ybk.ybk_id
				where ygt.tenant_id = 'SIPGLJ' and wyg.wyg_termcd = 'L'
				group by wyg.wyg_gtypecd, ybk.ybk_name, trade_type
			)
			select 
				IFNULL(pck.pck_stat_code ,pck.pck_kind_code) as 大货类, res.场地区域, res.trade_type,
				sum(res.gtpks) as 库场件数, sum(res.gtwg) as 库场重量, sum(res.gtvol) as 库场体积
			from res
			left join ODS_BLJ_PUB_CARGO_KIND_DF pck on res.货类代码 = pck.pck_kind_code
			group by 大货类, res.场地区域, res.trade_type
		)
		SELECT pck2.pck_kind_name as 大货类, cname.场地区域, 库场件数 ,库场重量 ,库场体积, cname.trade_type as 贸易类型
		from cname
		left join ODS_BLJ_PUB_CARGO_KIND_DF pck2 on cname.大货类 = pck2.pck_kind_code
	),
	tomonth as(
		with res as(
			select IFNULL(pck.pck_stat_code ,pck.pck_kind_code) as 大货类 , ybk.ybk_name as 场地区域,
			(case when goa.goa_iofg='1' then '进' when goa.goa_iofg='2' then '出' end) as 进出标志, DATE_FORMAT(goa_opdate,'%Y-%m') as mon,
				SUM(goa.goa_gtpks) as gtpks, SUM(goa.goa_gtwg) as gtwg, SUM(goa.goa_gtvol) as gtvol, voy.voy_trade as trade_type
			from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
			left join ODS_BLJ_WMS_YARD_GOODS_DF wyg on goa.goa_wyg_id  = wyg.wyg_id
			left join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id, wyg.wyg_evoy_id) = voy.voy_id
			left join ODS_BLJ_WMS_YARD_GOODS_DTL_DI ygt on goa.goa_ygt_id = ygt.ygt_id
			left join ODS_BLJ_PUB_CARGO_KIND_DF pck on wyg.wyg_gtypecd  = pck.pck_kind_code
			left join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = ygt.ygt_ygo_id
			left join ODS_BLJ_PUB_YARD_GOODS_LOCATION_DF ygc on ygo.ygo_ygc_id = ygc.ygc_id
			left join ODS_BLJ_PUB_YARD_BASE_BLOCK_DF ybk on ygc.ygc_ybk_id = ybk.ybk_id
			where goa.tenant_id = 'SIPGLJ' and wyg.wyg_termcd = 'L' and goa.goa_iofg<>0
			group by 大货类 , goa.goa_iofg, DATE_FORMAT(goa_opdate,'%Y-%m'), ybk.ybk_name, trade_type
		)
		select pck2.pck_kind_name as 大货类, res.场地区域, res.mon as 日期, res.trade_type as 贸易类型,
			res.进出标志, res.gtpks as 进出件数, res.gtwg as 进出重量, res.gtvol as 进出体积
		from res
		left join ODS_BLJ_PUB_CARGO_KIND_DF pck2 on res.大货类 = pck2.pck_kind_code
	)
	select tomonth.大货类, tomonth.场地区域, tomonth.日期 as 年月, tomonth.贸易类型, tomonth.进出标志, tomonth.进出件数, tomonth.进出重量,
		nowstore.库场件数, nowstore.库场重量
	from tomonth
	left join nowstore on nowstore.大货类=tomonth.大货类 and nowstore.场地区域=tomonth.场地区域 and nowstore.贸易类型=tomonth.贸易类型
	union all
	select tomonth.大货类, '全部' as 场地区域, tomonth.日期 as 年月, tomonth.贸易类型, tomonth.进出标志, SUM(tomonth.进出件数), SUM(tomonth.进出重量),
		SUM(nowstore.库场件数), SUM(nowstore.库场重量)
	from tomonth
	left join nowstore on nowstore.大货类=tomonth.大货类 and nowstore.场地区域=tomonth.场地区域 and nowstore.贸易类型=tomonth.贸易类型
	group by tomonth.日期,tomonth.大货类, tomonth.贸易类型, tomonth.进出标志
)
select *
from finaldata
where finaldata.年月 = DATE_FORMAT('{workdate}','%Y-%m') and finaldata.场地区域 = '{ybkname}'
order by finaldata.大货类, finaldata.贸易类型, finaldata.进出标志;