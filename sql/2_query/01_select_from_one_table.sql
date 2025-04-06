\connect ups_system_db

SELECT insurance_amt, item_num, final_delivery_date
FROM shipped_items
WHERE insurance_amt > 1000000
  AND final_delivery_date BETWEEN '2000-01-12' and '2010-12-31';