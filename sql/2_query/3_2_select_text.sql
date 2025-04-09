\connect ups_system_db

SET enable_indexscan = on;
SET enable_bitmapscan = on;

SELECT transportation_event_seq_number, comment
FROM item_transportations
WHERE to_tsvector('russian', comment) @@
      (phraseto_tsquery('russian', 'механический товар') && to_tsquery('russian', 'провал | угроза | пропадать'));
