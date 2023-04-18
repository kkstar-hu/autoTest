-- 昼夜工时表-员工
select pws.pws_voy_id as 航次, wsm.wsm_route_sign as 作业路标识,
	(case when wsm.wsm_type='L' then '理货员' when wsm.wsm_type='D' then '司机' when wsm.wsm_type='G' then '队关' end) as 类型,
	wsm.wsw_empno as 工号, wsm.wsm_gtpks as 件数, wsm.wsm_gtwg as 吨位, wsm.wsm_work_hour as 工作时间,
	wsm.wsm_truck_order as 车次, wsm.wsm_base_hour as 原始工时, wsm.wsm_real_hour as 折算工时, wsm.wsm_factor as 系数,
	wsm.wsm_adjust_factor as 调节系数, wsm.wsm_plus_minus_hour as 加减工时, wsm.wsm_plus_minus_rate as 加班率,wsm.wsm_percentage as 百分比
from ODS_BLJ_PWS_WORK_SHEET_MACHINE_DF wsm
join ODS_BLJ_PWS_WORK_SHEET_DF pws on wsm.wsm_pws_id  = pws.pws_id
where wsm.tenant_id = 'SIPGLJ' and pws.pws_hr_audit_tag = 'Y' and wsm.wsm_quo_id is not null and wsm.wsm_quo_id <> ''
    and DATE_FORMAT(pws.pws_opdate ,'%Y-%m-%d')>='{startdate}' and DATE_FORMAT(pws.pws_opdate ,'%Y-%m-%d')<='{enddate}'
	and pws.pws_voy_id = '{pws_voy_id}' {route_sign}
order by wsm.wsm_route_sign;