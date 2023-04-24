-- 装卸队
select pws.pws_voy_id as 航次, wsw.wsw_route_sign as 作业路标识, pck.pck_kind_name as 货名, pkg.pkg_cnname as 包装, wsw.wsw_gtpks as 件数, wsw.wsw_gtwg as 吨位,
	wsw.wsw_ptwg as 件重, pwl.pwl_name as 重量分类, opc.opc_code as 操作过程,
	wsw.wsw_oper_start_point as 起点, wsw.wsw_start_point_down as 起点下舱,
	wsw.wsw_oper_end_point as 终点, wsw.wsw_end_point_down as 终点下舱, wsw.wsw_oper_horizontal as 水平,
	wsw.wsw_work_hour as 工作时间,wsw.wsw_quotano as 定额编号, wsw.wsw_work_num as 计时工人数,
	wsw.wsw_plus_minus_hour as 工时加减, wsw.wsw_adjust_factor as 调节系数, wsw.wsw_overtime_rate as 加班率,
	wsw.wsw_tc_tag as 抬铲, wsw.wsw_td_tag as 抬吊, wsw.wsw_worker_complemen as 加人,
	wsw.wsw_base_hour as 原始工时, wsw.wsw_real_hour as 折算工时, wsw.wsw_remark as 备注
from ODS_BLJ_PWS_WORK_SHEET_WK_DF wsw
join ODS_BLJ_PWS_WORK_SHEET_DF pws on wsw.wsw_pws_id = pws.pws_id
join ODS_BLJ_PUB_CARGO_KIND_DF pck on wsw.wsw_gtypecd = pck.pck_kind_code and wsw.tenant_id = pck.tenant_id
join ODS_BLJ_PUB_PACKAGE_DF pkg on wsw.wsw_pktype = pkg.pkg_code and wsw.tenant_id = pkg.tenant_id
join ODS_BLJ_PUB_WEIGHT_LEVEL_DF pwl on wsw.wsw_weight_level = pwl.pwl_code and wsw.tenant_id = pwl.tenant_id
join ODS_BLJ_PUB_OPPROC_DF opc on wsw.wsw_opproc = opc.opc_id and wsw.tenant_id = opc.tenant_id
where wsw.tenant_id = 'SIPGLJ' and pws.pws_hr_audit_tag = 'Y' and wsw.wsw_quo_id is not null and wsw.wsw_quo_id <> ''
	and DATE_FORMAT(pws.pws_opdate ,'%Y-%m-%d')>='{startdate}' and DATE_FORMAT(pws.pws_opdate ,'%Y-%m-%d')<='{enddate}'
	and pws.pws_voy_id = '{pws_voy_id}' {route_sign}
order by wsw.wsw_route_sign;