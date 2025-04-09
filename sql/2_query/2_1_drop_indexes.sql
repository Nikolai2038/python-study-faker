\connect ups_system_db

DROP INDEX IF EXISTS idx_shipped_items_final_delivery_date;
DROP INDEX IF EXISTS idx_shipped_items_weight;
DROP INDEX IF EXISTS idx_shipped_items_retail_center_id;
DROP INDEX IF EXISTS idx_transportation_events_type;
DROP INDEX IF EXISTS idx_retail_centers_name;

ANALYSE;
