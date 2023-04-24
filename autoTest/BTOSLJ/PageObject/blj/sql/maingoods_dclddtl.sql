-- 主要货种完成量
with uni as(
	with fnl as(
		with res as(
			select DATE_FORMAT(goa.goa_opdate ,'%m') as 月份, DATE_FORMAT(goa.goa_opdate ,'%Y') as 年份, SUM(goa.goa_gtwg)/10000 as 吨位,
				(case when voy.voy_iefg = 'I' then '外贸进口' when voy.voy_iefg = 'E' then '外贸出口'
				when wyg.wyg_gtypecd = 'CN' then '集装箱' end) as 性质,
				(case when voy.voy_iefg = 'I' and wyg.wyg_gtypecd = '1511' then '纸浆'
					  when voy.voy_iefg = 'I' and wyg.wyg_gtypecd like '041%' then '钢材'
					  when voy.voy_iefg = 'I' and wyg.wyg_gtypecd like '12%' then '设备'
					  when voy.voy_iefg = 'I' and wyg.wyg_gtypecd like '14%' then '有色金属'
					  when voy.voy_iefg = 'E' and wyg.wyg_gtypecd like '041%' then '钢材'
					  when voy.voy_iefg = 'E' and wyg.wyg_gtypecd like '12%' then '设备'
					  when voy.voy_iefg = 'E' and wyg.wyg_pktype = 'DD' then '吨袋'
					  when voy.voy_iefg = 'E' and wyg.wyg_gtypecd like '14%' then '有色金属'
					  when wyg.wyg_gtypecd = 'CN' then '集装箱'
					  else '其他' end) as 主要货种
			from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
			join ODS_BLJ_BPS_VOYAGE_DF voy on goa.goa_voy_id = voy.voy_id
			join ODS_BLJ_WMS_YARD_GOODS_DF wyg on goa.goa_wyg_id = wyg.wyg_id
			where voy.voy_trade = 'W' and goa.goa_optype in ('DC', 'LD')
			group by DATE_FORMAT(goa.goa_opdate ,'%Y'),DATE_FORMAT(goa.goa_opdate ,'%m'),性质, 主要货种
			union all
			select DATE_FORMAT(goa.goa_opdate ,'%m') as 月份, DATE_FORMAT(goa.goa_opdate ,'%Y') as 年份, SUM(goa.goa_gtwg)/10000 as 吨位, '内贸' as 性质,
				(case when wyg.wyg_gtypecd = 'CN' then '集装箱'
					  when por.pot_cnname = '曹妃甸' then '曹妃甸'
					  when por.pot_cnname = '鲅鱼圈' then '鲅鱼圈'
					  when por.pot_cnname = '大连' then '大连'
					  else '其他' end) as 主要货种
			from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
			join ODS_BLJ_BPS_VOYAGE_DF voy on goa.goa_voy_id = voy.voy_id
			join ODS_BLJ_WMS_YARD_GOODS_DF wyg on goa.goa_wyg_id = wyg.wyg_id
			left join ODS_BLJ_BUS_GOODS_DF gds on gds.gds_id  = wyg.wyg_gds_id
			left join ODS_BLJ_BUS_BILLS_DF bil on gds.gds_bil_id = bil.bil_id
			left join ODS_BLJ_PUB_PORTS_DF por on bil.bil_load_port = por.pot_portcd
			where voy.voy_trade = 'N' and goa.goa_optype in ('DC', 'LD')
			group by DATE_FORMAT(goa.goa_opdate ,'%Y'), DATE_FORMAT(goa.goa_opdate ,'%m'),性质, 主要货种
		)
	select res.年份, res.月份, res.吨位, res.性质, res.主要货种
	from res
	where res.主要货种 not in('集装箱', '其他')
	union all
	select res.年份, res.月份, SUM(res.吨位) as 吨位,'集装箱' as 性质, '集装箱' as 主要货种
	from res
	where res.主要货种 ='集装箱'
	group by res.年份, res.月份
	union all
	select res.年份, res.月份, SUM(res.吨位) as 吨位,'内外贸其他' as 性质, '其他' as 主要货种
	from res
	where res.主要货种 ='其他'
	group by res.年份, res.月份
	)
	select fnl.性质, fnl.主要货种, fnl.年份, fnl.吨位,
		(case when fnl.月份='01' then fnl.吨位 else 0 end) as gtwg_01,
		(case when fnl.月份='02' then fnl.吨位 else 0 end) as gtwg_02,
		(case when fnl.月份='03' then fnl.吨位 else 0 end) as gtwg_03,
		(case when fnl.月份='04' then fnl.吨位 else 0 end) as gtwg_04,
		(case when fnl.月份='05' then fnl.吨位 else 0 end) as gtwg_05,
		(case when fnl.月份='06' then fnl.吨位 else 0 end) as gtwg_06,
		(case when fnl.月份='07' then fnl.吨位 else 0 end) as gtwg_07,
		(case when fnl.月份='08' then fnl.吨位 else 0 end) as gtwg_08,
		(case when fnl.月份='09' then fnl.吨位 else 0 end) as gtwg_09,
		(case when fnl.月份='10' then fnl.吨位 else 0 end) as gtwg_10,
		(case when fnl.月份='11' then fnl.吨位 else 0 end) as gtwg_11,
		(case when fnl.月份='12' then fnl.吨位 else 0 end) as gtwg_12
	from fnl
)
select uni.性质, uni.主要货种, uni.年份, SUM(gtwg_01) as 1月, SUM(gtwg_02) as 2月, SUM(gtwg_03) as 3月, SUM(gtwg_04) as 4月,
	SUM(gtwg_05) as 5月, SUM(gtwg_06) as 6月, SUM(gtwg_07) as 7月, SUM(gtwg_08) as 8月, SUM(gtwg_09) as 9月, SUM(gtwg_10) as 10月,
	SUM(gtwg_11) as 11月, SUM(gtwg_12) as 12月, SUM(uni.吨位) as 合计, IFNULL(yes.一月,0) as 去年1月, IFNULL(yes.二月,0) as 去年2月
	, IFNULL(yes.三月,0) as 去年3月, IFNULL(yes.四月,0) as 去年4月, IFNULL(yes.五月,0) as 去年5月, IFNULL(yes.六月,0) as 去年6月
	, IFNULL(yes.七月,0) as 去年7月, IFNULL(yes.八月,0) as 去年8月, IFNULL(yes.九月,0) as 去年9月, IFNULL(yes.十月,0) as 去年10月
	, IFNULL(yes.十一月,0) as 去年11月, IFNULL(yes.十二月,0) as 去年12月, IFNULL(yes.合计,0) as 去年合计
from uni
left join (
	select uni.性质, uni.主要货种, uni.年份, SUM(gtwg_01) as 一月, SUM(gtwg_02) as 二月, SUM(gtwg_03) as 三月, SUM(gtwg_04) as 四月,
	SUM(gtwg_05) as 五月, SUM(gtwg_06) as 六月, SUM(gtwg_07) as 七月, SUM(gtwg_08) as 八月, SUM(gtwg_09) as 九月, SUM(gtwg_10) as 十月,
	SUM(gtwg_11) as 十一月, SUM(gtwg_12) as 十二月, SUM(uni.吨位) as 合计
	from uni
	where uni.年份 = '{yyyy2}'
	group by uni.年份, uni.性质, uni.主要货种
) yes on uni.性质=yes.性质 and uni.主要货种=yes.主要货种
where uni.年份 = '{yyyy1}'
group by uni.年份, uni.性质, uni.主要货种, yes.一月,yes.二月,yes.三月,yes.四月,yes.五月,yes.六月,
	yes.七月,yes.八月,yes.九月,yes.十月,yes.十一月,yes.十二月 ,yes.合计
order by uni.性质, uni.主要货种, uni.年份
;