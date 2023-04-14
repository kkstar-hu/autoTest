-- 昼夜工时表
with daywork as(
with shift1 as(
	select DATE_FORMAT(pws.pws_opdate,'%Y-%m-%d') as 日期, '工人' as 组别 , (case when pws.pws_shift='1' then '夜班' when pws.pws_shift='2' then '白班' end) as 时间,
	    sum(case when pws_type = 'N' or pws_type = 'W' then wsw_gtwg else 0 end)      as 大船吨位,
	    sum(case when pws_type = 'N' or pws_type = 'W' then wsw_real_hour else 0 end) as 大船工时,
	    sum(case when pws_type = 'N' then wsw_gtwg else 0 end)                        as 内贸吨位,
	    sum(case when pws_type = 'N' then wsw_real_hour else 0 end)                   as 内贸工时,
		sum(case when pws_type = 'W' then wsw_gtwg else 0 end)                        as 外贸吨位,
	    sum(case when pws_type = 'W' then wsw_real_hour else 0 end)                   as 外贸工时,
	    sum(case when pws_type = 'B' then wsw_gtwg else 0 end)                        as 内河驳吨位,
	    sum(case when pws_type = 'B' then wsw_real_hour else 0 end)                   as 内河驳工时,
	    sum(case when pws_type = 'Y' then wsw_gtwg else 0 end)                        as 进出栈吨位,
	    sum(case when pws_type = 'Y' then wsw_real_hour else 0 end)                   as 进出栈工时,
	    sum(case when pws_type = 'Z' then wsw_gtwg else 0 end)                        as 杂项吨位,
	    sum(case when pws_type = 'Z' then wsw_real_hour else 0 end)                   as 杂项工时
	from ODS_BLJ_PWS_WORK_SHEET_WK_DF wsw
	left join ODS_BLJ_PWS_WORK_SHEET_DF pws on wsw.wsw_pws_id = pws.pws_id
	where pws.pws_hr_audit_tag ='Y'
	group by pws.pws_shift, pws.pws_opdate
	order by pws.pws_shift asc, pws.pws_opdate desc
	limit 9999
), shift2 as (
	select DATE_FORMAT(pws.pws_opdate,'%Y-%m-%d') as 日期, (case when wsm.wsm_type = 'L' then '理货员' else '队关' end) as 组别,
			(case when pws.pws_shift='1' then '夜班' when pws.pws_shift='2' then '白班' end) as 时间,
		    sum(case when pws_type = 'N' or pws_type = 'W' then wsm_gtwg else 0 end)      as 大船吨位,
		    sum(case when pws_type = 'N' or pws_type = 'W' then wsm_real_hour else 0 end) as 大船工时,
		    sum(case when pws_type = 'N' then wsm_gtwg else 0 end)                        as 内贸吨位,
		    sum(case when pws_type = 'N' then wsm_real_hour else 0 end)                   as 内贸工时,
			sum(case when pws_type = 'W' then wsm_gtwg else 0 end)                        as 外贸吨位,
		    sum(case when pws_type = 'W' then wsm_real_hour else 0 end)                   as 外贸工时,
		    sum(case when pws_type = 'B' then wsm_gtwg else 0 end)                        as 内河驳吨位,
		    sum(case when pws_type = 'B' then wsm_real_hour else 0 end)                   as 内河驳工时,
		    sum(case when pws_type = 'Y' then wsm_gtwg else 0 end)                        as 进出栈吨位,
		    sum(case when pws_type = 'Y' then wsm_real_hour else 0 end)                   as 进出栈工时,
		    sum(case when pws_type = 'Z' then wsm_gtwg else 0 end)                        as 杂项吨位,
		    sum(case when pws_type = 'Z' then wsm_real_hour else 0 end)                   as 杂项工时
	from ODS_BLJ_PWS_WORK_SHEET_MACHINE_DF wsm
	left join ODS_BLJ_PWS_WORK_SHEET_WK_DF wsw on wsm.wsm_wsw_id = wsw.wsw_id
	left join ODS_BLJ_PWS_WORK_SHEET_DF pws on wsm.wsm_pws_id = pws.pws_id
	where (wsm.wsm_type = 'G' or wsm.wsm_type = 'L') and pws.pws_hr_audit_tag ='Y'
	group by wsm.wsm_type, pws.pws_opdate, pws.pws_shift
	order by wsm.wsm_type, pws.pws_opdate desc, pws.pws_shift
	limit 9999
), shift3 as(
	select DATE_FORMAT(pws.pws_opdate,'%Y-%m-%d') as 日期, (case when dept1.dept_name='流机队' or dept2.dept_name ='流机队' then '机械队'
		when dept1.dept_name='门机队' or dept2.dept_name ='门机队' then '门机队'end) as 组别,
		(case when pws.pws_shift='1' then '夜班' when pws.pws_shift='2' then '白班' end) as 时间,
		sum(case when pws_type = 'N' or pws_type = 'W' then wsm_gtwg else 0 end)      as 大船吨位,
		sum(case when pws_type = 'N' or pws_type = 'W' then wsm_real_hour else 0 end) as 大船工时,
		sum(case when pws_type = 'N' then wsm_gtwg else 0 end)                        as 内贸吨位,
		sum(case when pws_type = 'N' then wsm_real_hour else 0 end)                   as 内贸工时,
		sum(case when pws_type = 'W' then wsm_gtwg else 0 end)                        as 外贸吨位,
		sum(case when pws_type = 'W' then wsm_real_hour else 0 end)                   as 外贸工时,
		sum(case when pws_type = 'B' then wsm_gtwg else 0 end)                        as 内河驳吨位,
		sum(case when pws_type = 'B' then wsm_real_hour else 0 end)                   as 内河驳工时,
		sum(case when pws_type = 'Y' then wsm_gtwg else 0 end)                        as 进出栈吨位,
		sum(case when pws_type = 'Y' then wsm_real_hour else 0 end)                   as 进出栈工时,
		sum(case when pws_type = 'Z' then wsm_gtwg else 0 end)                        as 杂项吨位,
		sum(case when pws_type = 'Z' then wsm_real_hour else 0 end)                   as 杂项工时
	from ODS_BLJ_PWS_WORK_SHEET_MACHINE_DF wsm
	left join ODS_BLJ_PWS_WORK_SHEET_WK_DF wsw on wsm.wsm_wsw_id = wsw.wsw_id
	left join ODS_BLJ_PWS_WORK_SHEET_DF pws on wsm.wsm_pws_id = pws.pws_id
	left join ODS_BLJ_SYS_DEPT_DF dept1 on wsm.wsm_dept_id = dept1.dept_id
	left join ODS_BLJ_SYS_DEPT_DF dept2 on dept2.dept_id  = dept1.dept_superior_id
	where wsm.wsm_type = 'D' and pws.pws_hr_audit_tag ='Y'
	group by pws.pws_opdate, pws.pws_shift, 组别
	order by pws.pws_opdate desc, pws.pws_shift, 组别
	limit 9999
)
select shift1.日期, '工人' as 组别 , '昼夜' as 时间,
    sum(shift1.大船吨位) as 大船吨位, sum(shift1.大船工时) as 大船工时,
    sum(shift1.内贸吨位) as 内贸吨位, sum(shift1.内贸工时) as 内贸工时,
	sum(shift1.外贸吨位) as 外贸吨位, sum(shift1.外贸工时) as 外贸工时,
    sum(shift1.内河驳吨位) as 内河驳吨位, sum(shift1.内河驳工时) as 内河驳工时,
    sum(shift1.进出栈吨位) as 进出栈吨位, sum(shift1.进出栈工时) as 进出栈工时,
    sum(shift1.杂项吨位) as 杂项吨位, sum(shift1.杂项工时) as 杂项工时
from shift1
group by shift1.日期
order by shift1.日期 desc
union all
select * from shift1
union all
select shift2.日期, shift2.组别 , '昼夜' as 时间,
    sum(shift2.大船吨位) as 大船吨位, sum(shift2.大船工时) as 大船工时,
    sum(shift2.内贸吨位) as 内贸吨位, sum(shift2.内贸工时) as 内贸工时,
	sum(shift2.外贸吨位) as 外贸吨位, sum(shift2.外贸工时) as 外贸工时,
    sum(shift2.内河驳吨位) as 内河驳吨位, sum(shift2.内河驳工时) as 内河驳工时,
    sum(shift2.进出栈吨位) as 进出栈吨位, sum(shift2.进出栈工时) as 进出栈工时,
    sum(shift2.杂项吨位) as 杂项吨位, sum(shift2.杂项工时) as 杂项工时
from shift2
group by shift2.日期, shift2.组别
order by shift2.日期 desc, shift2.组别
union all
select * from shift2
union all
select shift3.日期, shift3.组别 , '昼夜' as 时间,
    sum(shift3.大船吨位) as 大船吨位, sum(shift3.大船工时) as 大船工时,
    sum(shift3.内贸吨位) as 内贸吨位, sum(shift3.内贸工时) as 内贸工时,
	sum(shift3.外贸吨位) as 外贸吨位, sum(shift3.外贸工时) as 外贸工时,
    sum(shift3.内河驳吨位) as 内河驳吨位, sum(shift3.内河驳工时) as 内河驳工时,
    sum(shift3.进出栈吨位) as 进出栈吨位, sum(shift3.进出栈工时) as 进出栈工时,
    sum(shift3.杂项吨位) as 杂项吨位, sum(shift3.杂项工时) as 杂项工时
from shift3
group by shift3.日期, shift3.组别
order by shift3.日期 desc, shift3.组别
union all
select * from shift3)
select *
from daywork
where daywork.日期='2023-04-10'
union all
select DATE_FORMAT(daywork.日期,'%Y-%m') as 日期, daywork.组别, '月度' as 时间,
	sum(daywork.大船吨位) as 大船吨位, sum(daywork.大船工时) as 大船工时,
    sum(daywork.内贸吨位) as 内贸吨位, sum(daywork.内贸工时) as 内贸工时,
	sum(daywork.外贸吨位) as 外贸吨位, sum(daywork.外贸工时) as 外贸工时,
    sum(daywork.内河驳吨位) as 内河驳吨位, sum(daywork.内河驳工时) as 内河驳工时,
    sum(daywork.进出栈吨位) as 进出栈吨位, sum(daywork.进出栈工时) as 进出栈工时,
    sum(daywork.杂项吨位) as 杂项吨位, sum(daywork.杂项工时) as 杂项工时
from daywork
where daywork.日期>='2023-04-01' and daywork.日期<='2023-04-10' and daywork.时间='昼夜'
group by daywork.组别, DATE_FORMAT(daywork.日期,'%Y-%m')
union all
select DATE_FORMAT(daywork.日期,'%Y') as 日期, daywork.组别, '年度' as 时间,
	sum(daywork.大船吨位) as 大船吨位, sum(daywork.大船工时) as 大船工时,
    sum(daywork.内贸吨位) as 内贸吨位, sum(daywork.内贸工时) as 内贸工时,
	sum(daywork.外贸吨位) as 外贸吨位, sum(daywork.外贸工时) as 外贸工时,
    sum(daywork.内河驳吨位) as 内河驳吨位, sum(daywork.内河驳工时) as 内河驳工时,
    sum(daywork.进出栈吨位) as 进出栈吨位, sum(daywork.进出栈工时) as 进出栈工时,
    sum(daywork.杂项吨位) as 杂项吨位, sum(daywork.杂项工时) as 杂项工时
from daywork
where daywork.日期>='2023-01-01' and daywork.日期<='2023-04-10' and daywork.时间='昼夜'
group by daywork.组别, DATE_FORMAT(daywork.日期,'%Y')
union all
select daywork.日期, '合计' as 组别, daywork.时间,
	sum(daywork.大船吨位) as 大船吨位, sum(daywork.大船工时) as 大船工时,
    sum(daywork.内贸吨位) as 内贸吨位, sum(daywork.内贸工时) as 内贸工时,
	sum(daywork.外贸吨位) as 外贸吨位, sum(daywork.外贸工时) as 外贸工时,
    sum(daywork.内河驳吨位) as 内河驳吨位, sum(daywork.内河驳工时) as 内河驳工时,
    sum(daywork.进出栈吨位) as 进出栈吨位, sum(daywork.进出栈工时) as 进出栈工时,
    sum(daywork.杂项吨位) as 杂项吨位, sum(daywork.杂项工时) as 杂项工时
from daywork
where daywork.日期='2023-04-10'
group by daywork.日期, daywork.时间
union all
select DATE_FORMAT(daywork.日期,'%Y-%m') as 日期, '合计' as 组别, '月度' as 时间,
	sum(daywork.大船吨位) as 大船吨位, sum(daywork.大船工时) as 大船工时,
    sum(daywork.内贸吨位) as 内贸吨位, sum(daywork.内贸工时) as 内贸工时,
	sum(daywork.外贸吨位) as 外贸吨位, sum(daywork.外贸工时) as 外贸工时,
    sum(daywork.内河驳吨位) as 内河驳吨位, sum(daywork.内河驳工时) as 内河驳工时,
    sum(daywork.进出栈吨位) as 进出栈吨位, sum(daywork.进出栈工时) as 进出栈工时,
    sum(daywork.杂项吨位) as 杂项吨位, sum(daywork.杂项工时) as 杂项工时
from daywork
where daywork.日期>='2023-04-01' and daywork.日期<='2023-04-10' and daywork.时间='昼夜'
group by DATE_FORMAT(daywork.日期,'%Y-%m')
union all
select DATE_FORMAT(daywork.日期,'%Y') as 日期, '合计' as 组别, '年度' as 时间,
	sum(daywork.大船吨位) as 大船吨位, sum(daywork.大船工时) as 大船工时,
    sum(daywork.内贸吨位) as 内贸吨位, sum(daywork.内贸工时) as 内贸工时,
	sum(daywork.外贸吨位) as 外贸吨位, sum(daywork.外贸工时) as 外贸工时,
    sum(daywork.内河驳吨位) as 内河驳吨位, sum(daywork.内河驳工时) as 内河驳工时,
    sum(daywork.进出栈吨位) as 进出栈吨位, sum(daywork.进出栈工时) as 进出栈工时,
    sum(daywork.杂项吨位) as 杂项吨位, sum(daywork.杂项工时) as 杂项工时
from daywork
where daywork.日期>='2023-01-01' and daywork.日期<='2023-04-10' and daywork.时间='昼夜' and daywork.组别 is not null
group by DATE_FORMAT(daywork.日期,'%Y')
;