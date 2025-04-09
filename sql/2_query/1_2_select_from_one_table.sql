\connect ups_system_db

SET enable_indexscan = on;
SET enable_bitmapscan = on;

SELECT insurance_amt, item_num, final_delivery_date
FROM shipped_items
WHERE insurance_amt BETWEEN 3000000 AND 3100000
  AND final_delivery_date BETWEEN '2005-01-01 00:00:00+00'::timestamptz AND '2005-06-30 00:00:00+00'::timestamptz;