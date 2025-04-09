\connect ups_system_db

CREATE INDEX IF NOT EXISTS idx_shipped_items_final_delivery_date ON public.shipped_items(final_delivery_date);
CREATE INDEX IF NOT EXISTS idx_shipped_items_weight ON public.shipped_items(weight);
CREATE INDEX IF NOT EXISTS idx_shipped_items_retail_center_id ON public.shipped_items(retail_center_id);
CREATE INDEX IF NOT EXISTS idx_transportation_events_type ON public.transportation_events(type);
CREATE INDEX IF NOT EXISTS idx_retail_centers_name ON public.retail_centers(name);

ANALYSE;
