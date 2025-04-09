\connect ups_system_db

CREATE INDEX IF NOT EXISTS idx_insurance_amt ON shipped_items(insurance_amt);
CREATE INDEX IF NOT EXISTS idx_final_delivery_date ON shipped_items(final_delivery_date);

ANALYSE;
