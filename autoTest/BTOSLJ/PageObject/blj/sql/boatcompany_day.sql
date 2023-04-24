-- 船公司外贸进出口, 只统计有装卸船理货数据的航次
with finalres as(
	with res as(
		select wyg.wyg_id ,wyg.wyg_iefg ,wyg.wyg_ivoy_id ,wyg.wyg_evoy_id ,wyg.wyg_gtypecd ,pck_kind_name ,
			(case when (pck.pck_kind_code like '12%') then '外出设备'
				  when (pck.pck_kind_code like '041%') then '外出钢材'
				  when wyg.wyg_pktype = 'DD' then '外出吨袋货'
				  else '外出其他' end) as 货物分类
		from ODS_BLJ_WMS_YARD_GOODS_DF wyg
		join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id,wyg.wyg_evoy_id)=voy.voy_id
		join ODS_BLJ_PUB_CARGO_KIND_DF pck on wyg.wyg_gtypecd = pck.pck_kind_code and wyg.tenant_id = pck.tenant_id
		where wyg.wyg_iefg ='E' and voy.voy_trade = 'W' and wyg.tenant_id = 'SIPGLJ'
		union all
		select wyg.wyg_id ,wyg.wyg_iefg ,wyg.wyg_ivoy_id ,wyg.wyg_evoy_id ,wyg.wyg_gtypecd ,pck_kind_name ,
			(case when (pck.pck_kind_code like '12%') then '外进设备'
				  when (pck.pck_kind_code like '041%') then '外进钢材'
				  when pck.pck_kind_code = '1511' then '外进纸浆'
				  when pck.pck_kind_code = '071' then '外进原木'
				  else '外进其他' end) as 货物分类
		from ODS_BLJ_WMS_YARD_GOODS_DF wyg
		join ODS_BLJ_BPS_VOYAGE_DF voy on IFNULL(wyg.wyg_ivoy_id,wyg.wyg_evoy_id)=voy.voy_id
		join ODS_BLJ_PUB_CARGO_KIND_DF pck on wyg.wyg_gtypecd = pck.pck_kind_code and wyg.tenant_id = pck.tenant_id
		where wyg.wyg_iefg ='I' and voy.voy_trade = 'W' and wyg.tenant_id = 'SIPGLJ'
	)
	select DATE_FORMAT(goa.goa_opdate ,'%Y-%m') as 月份 ,
		(case when cstr.cst_shrtnm not in('宏大','G2','大连春安','SINOWAY','耀洋','中远海特',
 		'汉信船务','安顺','南京远洋','EPC','荷亚船务','中波','NYK','万立','哥伦比亚','友鸿','连云港中源',
 		'安闳船务','鸿优','韩国现代','弘发') then '其他' else cstr.cst_shrtnm end) as 船公司,
		count(distinct case when voy.voy_iefg ='I' then voy.voy_id else null end) as 进口艘次,
		count(distinct case when voy.voy_iefg ='E' then voy.voy_id else null end) as 出口艘次,
		-- count(distinct case when scd.scd_ivoyage is not null and scd.scd_ivoyage!='' then scd.scd_ivoyage else null end) as 进口艘次,
		-- count(distinct case when scd.scd_evoyage is not null and scd.scd_evoyage!='' then scd.scd_evoyage else null end) as 出口艘次,
		count(distinct voy.voy_id) as 合计艘次,
		SUM(case when res.wyg_iefg='E' and goa.goa_optype='LD' and res.货物分类='外出钢材'
			then goa.goa_gtwg else 0 end)/10000 as 外出钢材,
		SUM(case when res.wyg_iefg='E' and goa.goa_optype='LD' and res.货物分类='外出设备'
			then goa.goa_gtwg else 0 end)/10000 as 外出设备,
		SUM(case when res.wyg_iefg='E' and goa.goa_optype='LD' and res.货物分类='外出吨袋货'
			then goa.goa_gtwg else 0 end)/10000 as 外出吨袋货,
		SUM(case when res.wyg_iefg='E' and goa.goa_optype='LD' and res.货物分类='外出其他'
			then goa.goa_gtwg else 0 end)/10000 as 外出其他,
		SUM(case when res.wyg_iefg='E' and goa.goa_optype='LD'
			then goa.goa_gtwg else 0 end)/10000 as 外出小计,
		SUM(case when res.wyg_iefg='I' and goa.goa_optype='DC' and res.货物分类='外进纸浆'
			then goa.goa_gtwg else 0 end)/10000 as 外进纸浆,
		SUM(case when res.wyg_iefg='I' and goa.goa_optype='DC' and res.货物分类='外进钢材'
			then goa.goa_gtwg else 0 end)/10000 as 外进钢材,
		SUM(case when res.wyg_iefg='I' and goa.goa_optype='DC' and res.货物分类='外进设备'
			then goa.goa_gtwg else 0 end)/10000 as 外进设备,
		SUM(case when res.wyg_iefg='I' and goa.goa_optype='DC' and res.货物分类='外进原木'
			then goa.goa_gtwg else 0 end)/10000 as 外进原木,
		SUM(case when res.wyg_iefg='I' and goa.goa_optype='DC' and res.货物分类='外进其他'
			then goa.goa_gtwg else 0 end)/10000 as 外进其他,
		SUM(case when res.wyg_iefg='I' and goa.goa_optype='DC'
			then goa.goa_gtwg else 0 end)/10000 as 外进小计,
		SUM(goa.goa_gtwg)/10000 as 合计吨位,
		SUM(case when goa.goa_gtwg>goa.goa_gtvol
			then goa.goa_gtwg else goa.goa_gtvol end)/10000 as 合计计费吨
	from ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
	join res on goa.goa_wyg_id = res.wyg_id
	left join ODS_BLJ_BPS_VOYAGE_DF voy on goa.goa_voy_id = voy.voy_id
	join ODS_BLJ_BPS_SCHEDULE_DF scd on voy.voy_scd_id = scd.scd_id
	join ODS_BLJ_BPS_VESSELS_DF vsl on scd.scd_vsl_cd = vsl.vsl_cd and scd.tenant_id = vsl.tenant_id
	join (select cst_id, cst_cstmcd ,cst_shrtnm, cst.tenant_id
		  from ODS.ODS_BLJ_PUB_CUSTOMERS_DF cst
		  join ODS.ODS_BLJ_PUB_CUSTOMERS_ROLE_DF ctr on cst.cst_id=ctr.ctr_cst_id and cst.tenant_id = ctr.tenant_id
		  where ctr.ctr_cst_type ='VCM'
		  ) cstr on vsl.vsl_cst_shippingline = cstr.cst_cstmcd and vsl.tenant_id = cstr.tenant_id
	where goa.goa_optype in ('LD','DC')
	group by 船公司, DATE_FORMAT(goa.goa_opdate ,'%Y-%m')
)
select finalres.月份,finalres.船公司,finalres.进口艘次,finalres.出口艘次,finalres.合计艘次,res2.年度合计艘次,finalres.外出钢材,
finalres.外出设备,finalres.外出吨袋货,finalres.外出其他,finalres.外出小计,finalres.外进纸浆,finalres.外进钢材,finalres.外进设备,
finalres.外进原木,finalres.外进其他,finalres.外进小计,finalres.合计吨位,finalres.合计计费吨, res2.年度合计吨位 , res2.年度合计计费吨
from finalres
join (
		select 船公司, SUM(合计艘次) as 年度合计艘次, SUM(合计吨位) as 年度合计吨位, SUM(合计计费吨) as 年度合计计费吨
	  	from finalres
	  	group by DATE_FORMAT(月份 ,'%Y'), 船公司
	 ) res2 on finalres.船公司 = res2.船公司
where finalres.月份 = DATE_FORMAT('{workdate}' ,'%Y-%m')
;
