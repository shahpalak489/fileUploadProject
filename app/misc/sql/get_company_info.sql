select 
    cid,
	cname,
	convert(datetime, share_price_dt, 23) share_price_dt,
	convert(numeric(19, 2), share_price) share_price,
	comments,
	f_name
from 
    master.dbo.company_info_v2
where
	comments <> "new entry"
