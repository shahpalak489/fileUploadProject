with cte_max_runid as (
	select
		max(runid) runid
	from
		master.dbo.company_info
)
select 
    v.cid,
	v.cname,
	convert(datetime, v.share_price_dt, 23) share_price_dt,
	convert(numeric(19, 2), v.share_price) share_price,
	v.comments,
	v.f_name
from 
    master.dbo.company_info v
join
	cte_max_runid c on
		c.runid = v.runid
where 
	v.f_name is not null
order by
	v.share_price,
	v.cid
