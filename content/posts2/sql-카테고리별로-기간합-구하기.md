---
title: "[SQL] 카테고리별로 기간합 구하기"
lastmod: 2025-03-12T02:22:00.000Z
author: "Gunn Kim"
description: ""
notion_id: "1d91e9df-9028-45a7-a8ce-c4e32e3582c3"
---

```sql
select cate_fullpath,
	count(case when yyyy = 2019 then 1 end) as y2019,
	count(case when yyyy = 2020 then 1 end) as y2020,
	count(case when yyyy = 2019 and mm between 5 and 10 then 1 end) as may_y2019,
	count(case when yyyy = 2020 and mm between 5 and 10 then 1 end) as may_y2020,
	count(case when yyyy = 2019 and mm between 2 and 4 then 1 end) as feb_y2019,
	count(case when yyyy = 2020 and mm between 2 and 4 then 1 end) as feb_y2020
from navi.route_all
where yyyy between 2019 and 2020
and mm between 2 and 10
group by 1
```



