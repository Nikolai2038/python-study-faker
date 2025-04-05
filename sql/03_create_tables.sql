\connect ups_system_db

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS public.item_transportations
(
    transportation_event_seq_number integer NOT NULL,
    shipped_item_item_num           integer NOT NULL,
    comment                         character varying(255)
);

CREATE TABLE IF NOT EXISTS public.retail_centers
(
    id      integer NOT NULL,
    name    character varying(255),
    address character varying(255)
);

CREATE TABLE IF NOT EXISTS public.shipped_items
(
    item_num            integer NOT NULL,
    retail_center_id    integer,
    weight              numeric(19, 0),
    dimension           numeric(19, 0),
    insurance_amt       numeric(19, 0),
    destination         character varying(255),
    final_delivery_date timestamp without time zone
);

CREATE TABLE IF NOT EXISTS public.transportation_events
(
    seq_number     integer NOT NULL,
    type           character varying(255),
    delivery_route character varying(255)
);
