-- 内贸进口船舶作业情况统计
with finaldata as(
	with res as(
		select CD.vsl_cnname as 船名, CD.voy_voyage as 航次, CD.舱单件数, CD.舱单重量, IFNULL(GA.车直提件数,0) as 车直提件数,
			IFNULL(GA.车直提重量,0) as 车直提重量, IFNULL(GA.驳直提件数,0) as 驳直提件数, IFNULL(GA.驳直提重量,0) as 驳直提重量,
			IFNULL(GA.进场件数,0) as 进场件数, IFNULL(GA.进场重量,0) as 进场重量,
			IFNULL(GA.库场提货件数,0) as 库场提货件数, IFNULL(GA.库场提货重量,0) as 库场提货重量
		from(
			select vsl.vsl_cnname, voy.voy_id, voy.voy_voyage ,SUM(bil.bil_gtpks) as 舱单件数, SUM(bil.bil_gtwg) as 舱单重量
			from ODS_BLJ_BUS_BILLS_DF bil
			left join ODS_BLJ_BPS_VOYAGE_DF voy on bil.bil_voy_id = voy.voy_id
			left join ODS_BLJ_BPS_SCHEDULE_DF scd on voy.voy_scd_id = scd.scd_id
			left join ODS_BLJ_BPS_VESSELS_DF vsl  on scd.scd_vsl_cd = vsl.vsl_cd
			left join ODS_BLJ_BPS_VESSEL_BERTHES_DF vbt on voy.voy_scd_id = vbt.vbt_scd_id
			where bil.bil_bill_iefg = 'I' and bil.bil_bill_trade = 'N' and vsl.tenant_id = 'SIPGLJ'
				and DATE_FORMAT(vbt.vbt_abthdt,'%Y-%m-%d') <= '{endtm}'
				and DATE_FORMAT(vbt.vbt_abthdt,'%Y-%m-%d') >= '{starttm}'
			group by vsl.vsl_cnname, voy.voy_id, voy.voy_voyage
		) CD
		left join(
			select goa.goa_voy_id,
				SUM(case when goa.goa_optype = 'DC' and (goa.goa_opproc = '412' or goa.goa_opproc = '009')
			        then goa.goa_gtpks else 0 end) as 车直提件数,
			    SUM(case when goa.goa_optype = 'DC' and (goa.goa_opproc = '412' or goa.goa_opproc = '009')
			        then goa.goa_gtwg else 0 end) as 车直提重量,
			    SUM(case when goa.goa_optype = 'DC' and (goa.goa_opproc = '411' or goa.goa_opproc = '413'
			        or goa.goa_opproc = '181015' or goa.goa_opproc = '181014' or goa.goa_opproc = '012')
			        then goa.goa_gtpks else 0 end) as 驳直提件数,
			    SUM(case when goa.goa_optype = 'DC' and (goa.goa_opproc = '411' or goa.goa_opproc = '413'
			        or goa.goa_opproc = '181015' or goa.goa_opproc = '181014' or goa.goa_opproc = '012')
			        then goa.goa_gtwg else 0 end) as 驳直提重量,
			    SUM(case when goa.goa_optype = 'DC' and (goa.goa_opproc = '013' or goa.goa_opproc = '014')
			        then goa.goa_gtpks else 0 end) as 进场件数,
			    SUM(case when goa.goa_optype = 'DC' and (goa.goa_opproc = '013' or goa.goa_opproc = '014')
			        then goa.goa_gtwg else 0 end) as 进场重量,
			    SUM(case when goa.goa_optype = 'PK' and (goa.goa_opproc = '008' or goa.goa_opproc = '0081'
			    	or goa.goa_opproc = '011' or goa.goa_opproc = '010')
			    	then goa.goa_gtpks else 0 end) as 库场提货件数,
			    SUM(case when goa.goa_optype = 'PK' and (goa.goa_opproc = '008' or goa.goa_opproc = '0081'
			    	or goa.goa_opproc = '011' or goa.goa_opproc = '010')
			        then goa.goa_gtwg else 0 end) as 库场提货重量
			from ODS.ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa
			left join ODS_BLJ_WMS_YARD_GOODS_DF wyg on goa.goa_wyg_id = wyg.wyg_id
			where wyg.wyg_iefg = 'I'
			group by goa.goa_voy_id) GA
		on GA.goa_voy_id = CD.voy_id
	)
	select * from res
	union all
	select '合计' as 船名, '合计' as 航次, SUM(res.舱单件数), SUM(res.舱单重量), IFNULL(SUM(res.车直提件数),0), SUM(res.车直提重量),
		SUM(res.驳直提件数), SUM(res.驳直提重量), SUM(res.进场件数), SUM(res.进场重量), SUM(res.库场提货件数), SUM(res.库场提货重量)
	from res
)
select *, (finaldata.舱单件数-finaldata.车直提件数-finaldata.驳直提件数-finaldata.库场提货件数) as 剩余件数,
	(finaldata.舱单重量-finaldata.车直提重量-finaldata.驳直提重量-finaldata.库场提货重量) as 剩余重量
from finaldata;