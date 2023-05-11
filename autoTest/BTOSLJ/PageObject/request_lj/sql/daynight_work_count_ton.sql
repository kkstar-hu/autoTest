with res as(
	with plan as(
		SELECT COALESCE(ship.opdate,warehouse.opdate) AS 日期, '计划' AS 计实, COALESCE(ship.shift,warehouse.shift) AS 工班,
			COALESCE(ship.内贸, 0) AS 内贸, COALESCE(ship.外贸, 0) AS 外贸, COALESCE(warehouse.内河驳, 0) AS 内河驳, 0 as 中转,
			COALESCE(warehouse.进栈, 0) AS 进栈, COALESCE(warehouse.出栈, 0) AS 出栈
		FROM
		(
			select to_char(dvp_opdate,'yyyy-MM-dd') as opdate,
			(case when dvr.dvr_shift_no='1' then '夜班' when dvr.dvr_shift_no='2' then '日班' end) as shift,
			SUM(case when dvp.dvp_trade='N' then dvr.dvr_throughput else 0 end) as 内贸,
			SUM(case when dvp.dvp_trade='W' then dvr.dvr_throughput else 0 end) as 外贸
			from dts_vessel_plan dvp
			inner join dts_vessel_route dvr on dvr.dvr_dvp_id = dvp.dvp_id
			where dvr.dvr_termcd = 'L' and dvr.tenant_id ='SIPGLJ'
			group by opdate, shift
		) ship
		FULL OUTER JOIN
		(
			select to_char(dwp_opdate,'yyyy-MM-dd') as opdate,
			(case when dwr.dwr_shift_no='1' then '夜班' when dwr.dwr_shift_no='2' then '日班' end) as shift,
			SUM(case when dwp.dwp_type in('B','DB','H') then dwr.dwr_opton else 0 end) as 内河驳,
			SUM(case when dwp.dwp_type in('W','DW','HC') and pln.pln_transmode='DE' then dwr.dwr_opton else 0 end) as 进栈,
			SUM(case when dwp.dwp_type in('W','DW','HC') and pln.pln_transmode='PK' then dwr.dwr_opton else 0 end) as 出栈
			from dts_warehouse_plan dwp
			inner join dts_warehouse_route dwr on dwr.dwr_dwp_id = dwp.dwp_id
			inner join pas_plans pln on dwp.dwp_pln_id = pln.pln_id
			where dwr.dwr_termcd = 'L' and dwr.tenant_id ='SIPGLJ'
			group by opdate, shift
		) warehouse
		ON ship.opdate = warehouse.opdate and ship.shift = warehouse.shift
		ORDER BY 日期 desc
	),
	actual as(
		SELECT COALESCE(ship.opdate,warehouse.opdate) AS 日期, '实绩' AS 计实, COALESCE(ship.shift,warehouse.shift) AS 工班,
			COALESCE(ship.内贸, 0) AS 内贸, COALESCE(ship.外贸, 0) AS 外贸, COALESCE(warehouse.内河驳, 0) AS 内河驳,
			COALESCE(ship.中转, 0) as 中转, COALESCE(warehouse.进栈, 0) AS 进栈, COALESCE(warehouse.出栈, 0) AS 出栈,
			ship.vhr_ton
		FROM
		(
			select to_char(vhr_opdate,'yyyy-MM-dd') as opdate,
			(case when vhr_shift='1' then '夜班' when vhr_shift='2' then '日班' end) as shift,
			SUM(case when vhr_trade='N' then vhr_wl_cwgt else 0 end) as 内贸,
			SUM(case when vhr_trade='W' then vhr_wl_cwgt else 0 end) as 外贸,
			SUM(COALESCE(vhr_transit_ton, 0)) as 中转,
			SUM(case when vhr_ton_flag='Y' then vhr_transit_ton else 0 end) as vhr_ton
			from dts_vessel_hatch_report
			where vhr_termcd='L' and tenant_id='SIPGLJ'
			group by opdate, shift
		) ship
		FULL OUTER JOIN
		(
			select to_char(dst.dst_opdate,'yyyy-MM-dd') as opdate,
			(case when dwr_shift_no='1' then '夜班' when dwr_shift_no='2' then '日班' end) as shift,
			SUM(case when dwp.dwp_type in('B','DB','H') then stw.stw_r_gtwg else 0 end) as 内河驳,
			SUM(case when dwp.dwp_type in('W','DW','HC') and pln.pln_transmode='DE' then stw.stw_r_gtwg else 0 end) as 进栈,
			SUM(case when dwp.dwp_type in('W','DW','HC') and pln.pln_transmode='PK' then stw.stw_r_gtwg else 0 end) as 出栈
			from dts_shift_task_wkgroup stw
			join dts_shift_task dst on stw.stw_dst_id=dst.dst_id
			join dts_warehouse_route dwr on dwr.dwr_id=dst.dst_route_id
			join dts_warehouse_plan dwp on dwr.dwr_dwp_id=dwp.dwp_id
			join pas_plans pln on dwp.dwp_pln_id=pln.pln_id
			where dwr.dwr_termcd = 'L' and dwr.tenant_id ='SIPGLJ'
			group by opdate, shift
		) warehouse
		ON ship.opdate = warehouse.opdate and ship.shift = warehouse.shift
		ORDER BY 日期 desc
	)
	select 日期, 工班, 计实, 内贸, 外贸, 内河驳, 中转, 进栈, 出栈, 进栈+出栈 as 进出栈,
		内贸+外贸+内河驳+进栈+出栈 as 操作吨, 内贸+外贸+内河驳 as 吞吐量
	from plan
	union all
	select 日期, '合计' as 工班, 计实, sum(内贸), sum(外贸), sum(内河驳), sum(中转), sum(进栈), sum(出栈), sum(进栈)+sum(出栈) as 进出栈,
		sum(内贸)+sum(外贸)+sum(内河驳)+sum(进栈)+sum(出栈) as 操作吨, sum(内贸)+sum(外贸)+sum(内河驳) as 吞吐量
	from plan
	group by 日期, 计实
	union all
	select 日期, 工班, 计实, 内贸, 外贸, 内河驳, 中转, 进栈, 出栈, 进栈+出栈 as 进出栈,
		内贸+外贸+内河驳+进栈+出栈 as 操作吨, 内贸+外贸+内河驳+COALESCE(vhr_ton, 0) as 吞吐量
	from actual
	union all
	select 日期, '合计' as 工班, 计实, sum(内贸), sum(外贸), sum(内河驳), sum(中转), sum(进栈), sum(出栈), sum(进栈)+sum(出栈) as 进出栈,
		sum(内贸)+sum(外贸)+sum(内河驳)+sum(进栈)+sum(出栈) as 操作吨, sum(内贸)+sum(外贸)+sum(内河驳)+sum(COALESCE(vhr_ton, 0)) as 吞吐量
	from actual
	group by 日期, 计实
)
select '当天统计' as 日期, 工班, 计实, 内贸, 外贸, 内河驳, 中转, 进栈, 出栈, 进出栈, 操作吨, 吞吐量
from res
where (res.日期='{plan_date}' and res.计实='计划') or (res.日期='{actual_date}' and res.计实='实绩')
union all
select '月度统计' as 日期, 工班, 计实, SUM(内贸), SUM(外贸), SUM(内河驳), SUM(中转), SUM(进栈), SUM(出栈), SUM(进栈+出栈) as 进出栈,
		SUM(操作吨) as 操作吨, SUM(吞吐量) as 吞吐量
from res
where 日期>=to_char(date_trunc('MONTH','{plan_date}'::DATE),'yyyy-mm-dd') and 日期<='{plan_date}' and 计实='计划'
group by 工班, 计实
union all
select '月度统计' as 日期, 工班, 计实, SUM(内贸), SUM(外贸), SUM(内河驳), SUM(中转), SUM(进栈), SUM(出栈), SUM(进栈+出栈) as 进出栈,
		SUM(操作吨) as 操作吨, SUM(吞吐量) as 吞吐量
from res
where 日期>=to_char(date_trunc('MONTH','{actual_date}'::DATE),'yyyy-mm-dd') and 日期<='{actual_date}' and 计实='实绩'
group by 工班, 计实
union all
select '年度统计' as 日期, 工班, 计实, SUM(内贸), SUM(外贸), SUM(内河驳), SUM(中转), SUM(进栈), SUM(出栈), SUM(进栈+出栈) as 进出栈,
		SUM(操作吨) as 操作吨, SUM(吞吐量) as 吞吐量
from res
where 日期>=to_char(date_trunc('YEAR','{plan_date}'::DATE),'yyyy-mm-dd') and 日期<='{plan_date}' and 计实='计划'
group by 工班, 计实
union all
select '年度统计' as 日期, 工班, 计实, SUM(内贸), SUM(外贸), SUM(内河驳), SUM(中转), SUM(进栈), SUM(出栈), SUM(进栈+出栈) as 进出栈,
		SUM(操作吨) as 操作吨, SUM(吞吐量) as 吞吐量
from res
where 日期>=to_char(date_trunc('YEAR','{actual_date}'::DATE),'yyyy-mm-dd') and 日期<='{actual_date}' and 计实='实绩'
group by 工班, 计实;