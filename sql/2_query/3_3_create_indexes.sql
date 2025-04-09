\connect ups_system_db

CREATE INDEX IF NOT EXISTS idx_item_transportations_comment_fulltext ON public.item_transportations USING gin(to_tsvector('russian', comment));

ANALYSE;
