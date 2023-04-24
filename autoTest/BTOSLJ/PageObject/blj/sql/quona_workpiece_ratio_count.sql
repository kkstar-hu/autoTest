-- 分类定额效率统计，装卸队操作过程拼接
with finaldata as(
	with base as(
		select wsw.wsw_quotano as 定额编号 ,COUNT(1) as 使用次数, wli.wli_name as 定额分类, array_join(COLLECT_SET(opc.opc_name), ',') as 操作过程,
		quo.quo_time_quota as 工时定额, SUM(wsw.wsw_work_hour) as 作业小时, SUM(wsw.wsw_gtwg) as 完成操作吨,
		quo.quo_work_num as 定额装卸工人数, SUM(wsw.wsw_work_num) as 配工组别人数, ROUND(SUM(wsw.wsw_real_hour),2) as 实际工时,
		quo.quo_hatch_hour as 定额作业小时量
		from ODS_BLJ_PWS_WORK_SHEET_WK_DF wsw
		left join ODS_BLJ_PWS_QUOTA_DF quo on wsw.wsw_quo_id = quo.quo_id and wsw.tenant_id = quo.tenant_id
		left join ODS_BLJ_PWS_WORK_SHEET_DF pws on wsw.wsw_pws_id = pws.pws_id and wsw.tenant_id = pws.tenant_id
		left join ODS_BLJ_PUB_WEIGHT_LEVEL_ITEM_DF wli on quo.quo_gtypecd = wli.wli_id and quo.tenant_id = wli.tenant_id
		left join ODS_BLJ_PUB_OPPROC_DF opc on wsw.wsw_opproc  = opc.opc_code and wsw.tenant_id = opc.tenant_id
		where wsw_quo_id is not null and wsw_quo_id <> '' and pws.pws_hr_audit_tag = 'Y' and wsw.tenant_id = 'SIPGLJ'
			and DATE_FORMAT(wsw.wsw_work_start_time,'%Y-%m-%d') >= '{start_date}'
			and DATE_FORMAT(wsw.wsw_work_end_time,'%Y-%m-%d') <= '{end_date}'
		group by wsw_quotano, quo.quo_time_quota, quo.quo_hatch_hour, quo.quo_work_num, wli.wli_name
	)
	select base.定额编号 , base.使用次数 , base.定额分类, base.操作过程 , base.工时定额 , base.作业小时 , base.完成操作吨 , base.定额装卸工人数 ,
		   ROUND(base.配工组别人数*1./base.使用次数, 0) as 实际装卸工人数 ,
		   (base.完成操作吨*1.*base.工时定额) as 定额工时, base.实际工时,
		   base.定额作业小时量, ROUND(base.完成操作吨*1./base.作业小时, 2) as 实际作业小时量
	from base
)
select finaldata.定额编号 , finaldata.使用次数, finaldata.定额分类, finaldata.操作过程 , finaldata.工时定额 , finaldata.作业小时 , finaldata.完成操作吨 , finaldata.定额装卸工人数 ,
	   finaldata.实际装卸工人数 , finaldata.定额工时, finaldata.实际工时, finaldata.定额作业小时量, finaldata.实际作业小时量,
	   ROUND((finaldata.实际作业小时量*1./finaldata.定额作业小时量),2) as 定额完成率
from finaldata
order by finaldata.定额编号;