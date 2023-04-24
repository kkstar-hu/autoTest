-- 保税仓库库场情况
with res as(
	select bod_no as 项号,vsl.vsl_cnname as 船名, voy.voy_voyage as 航次, bil.bil_bill_nbr as 提单号, bod.bod_gname as 货名,
		bil.bil_gtpks as 总件数, bil.bil_gtwg as 总重量,
		SUM(distinct case when bod_id is not null then bod.bod_ntwg else 0 end) as 总净重,
		SUM(case when goa.goa_iofg='1' then goa.goa_gtpks else 0 end) as 进库件数,
		SUM(case when goa.goa_iofg='1' then goa.goa_gtwg  else 0 end) as 进库重量,
		SUM(case when goa.goa_iofg='2' then goa.goa_gtpks else 0 end) as 出库件数,
		SUM(case when goa.goa_iofg='2' then goa.goa_gtwg  else 0 end) as 出库重量
	from ODS_BLJ_BUS_BILL_BONDED_DF bod
	left join ODS_BLJ_BUS_BILLS_DF bil on bod.bod_bil_id = bil.bil_id
	left join ODS_BLJ_BPS_VOYAGE_DF voy on bil.bil_voy_id = voy.voy_id
	left join ODS_BLJ_BPS_SCHEDULE_DF scd on voy.voy_scd_id = scd.scd_id
	left join ODS_BLJ_BPS_VESSELS_DF vsl on vsl.vsl_cd = scd.scd_vsl_cd and vsl.tenant_id = scd.tenant_id
	left join ODS_BLJ_BUS_GOODS_DF gds on gds.gds_bil_id = bil.bil_id
	left join ODS.ODS_BLJ_WMS_YARD_GOODS_DF wyg on gds.gds_id = wyg.wyg_gds_id
	left join ODS.ODS_BLJ_WMS_YARD_GOODS_DTL_DI ygt on ygt.ygt_wyg_id = wyg.wyg_id
	left join ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa on goa.goa_ygt_id = ygt.ygt_id
	where bod.tenant_id = 'SIPGLJ'
	group by bod_id , bod_no, vsl.vsl_cnname,voy.voy_voyage, bil.bil_bill_nbr, bod.bod_gname,
		bil.bil_gtpks, bil.bil_gtwg
)
select res.项号, res.船名, res.航次, res.提单号,res.货名,res.总件数,res.总重量,res.总净重,res.进库件数,res.进库重量,
	res.出库件数,res.出库重量,(res.进库件数-res.出库件数) as 结存件数, (res.进库重量-res.出库重量) as 结存重量
from res;