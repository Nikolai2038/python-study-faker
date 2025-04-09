\connect ups_system_db

SET enable_indexscan = on;
SET enable_bitmapscan = on;

SELECT si.item_num,                   -- Номер отправленного товара
       si.destination,                -- Место назначения
       si.final_delivery_date,        -- Дата окончательной доставки
       si.weight,                     -- Вес отправленного товара
       si.insurance_amt,              -- Страховая сумма
       rc.name AS retail_center_name, -- Название розничного центра
       te.type AS event_type,         -- Тип транспортного события
       it.comment                     -- Комментарий к событию транспортировки
FROM public.shipped_items si
         INNER JOIN public.retail_centers rc
                    ON si.retail_center_id = rc.id -- Связь с розничным центром
         INNER JOIN public.item_transportations it
                    ON si.item_num = it.shipped_item_item_num -- Связь с транспортировкой товара
         INNER JOIN public.transportation_events te
                    ON it.transportation_event_seq_number = te.seq_number -- Связь с событием транспортировки
WHERE si.final_delivery_date >= '2025-01-01 00:00:00+00'::timestamptz -- Фильтрация по дате доставки
  AND si.weight > 29                                                  -- Фильтрация по весу
  AND te.type = 'Наступать.'                                          -- Фильтрация по типу события
  AND rc.name ILIKE '%ОАО%'; -- Фильтрация по названию центра (регистр не важен)
