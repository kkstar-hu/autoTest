-- 机械计划数量, 取实绩日期
select pmt.pmt_name as 名称, stm.stm_mac_type as 代码, SUM(stm.stm_mac_num) as 数量
from dts_shift_task_mactype stm
join dts_shift_task dst on stm.stm_dst_id = dst.dst_id
join pub_machine_type pmt on stm.stm_mac_type = pmt.pmt_type and stm.tenant_id = pmt.tenant_id
where dst.dst_opdate = '{actual_date}'
group by stm.stm_mac_type ,pmt.pmt_name, dst.dst_opdate;
