-- 昼夜作业情况统计-桩脚统计
select ybk.ybk_name as 场地区域, COUNT(distinct ygt_id) as 桩脚
from ODS_BLJ_WMS_YARD_GOODS_DTL_DI ygt
join ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa on goa.goa_ygt_id = ygt.ygt_id
join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = ygt.ygt_wyg_id
join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = ygt.ygt_ygo_id
join ODS_BLJ_WMS_YARD_GOODS_REVIEW_DF ygr on ygr.ygr_ygt_id = ygt.ygt_id
join ODS_BLJ_PUB_YARD_GOODS_LOCATION_DF ygc on ygc.ygc_id = ygo.ygo_ygc_id and ygc.tenant_id = ygo.tenant_id
join ODS_BLJ_PUB_YARD_BASE_BLOCK_DF ybk on ygc.ygc_ybk_id = ybk.ybk_id
where ygo_type not in ('DL', 'DU') and wyg.wyg_gtypecd = '1511' and ygr.ygr_review_type = '1'
	and substring(ybk_name,1,1) in('A','B','C','D','F','G') and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d') = '{workdate}'
group by ybk.ybk_name
order by ybk.ybk_name
union all
select '合计' as 场地区域, COUNT(distinct ygt_id)
from ODS_BLJ_WMS_YARD_GOODS_DTL_DI ygt
join ODS_BLJ_WMS_GOODS_OCCUPY_ACTIVITIES_DI goa on goa.goa_ygt_id = ygt.ygt_id
join ODS_BLJ_WMS_YARD_GOODS_DF wyg on wyg.wyg_id = ygt.ygt_wyg_id
join ODS_BLJ_WMS_YARD_GOODS_OCCUPY_DF ygo on ygo.ygo_id = ygt.ygt_ygo_id
join ODS_BLJ_WMS_YARD_GOODS_REVIEW_DF ygr on ygr.ygr_ygt_id = ygt.ygt_id
join ODS_BLJ_PUB_YARD_GOODS_LOCATION_DF ygc on ygc.ygc_id = ygo.ygo_ygc_id and ygc.tenant_id = ygo.tenant_id
join ODS_BLJ_PUB_YARD_BASE_BLOCK_DF ybk on ygc.ygc_ybk_id = ybk.ybk_id
where ygo_type not in ('DL', 'DU') and wyg.wyg_gtypecd = '1511' and ygr.ygr_review_type = '1'
	and substring(ybk_name,1,1) in('A','B','C','D','F','G') and DATE_FORMAT(goa.goa_opdate ,'%Y-%m-%d') = '{workdate}'
;