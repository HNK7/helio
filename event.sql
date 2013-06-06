--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: tourney_event; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tourney_event (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    start_at timestamp with time zone NOT NULL,
    tournament_id integer NOT NULL,
    division character varying(1) NOT NULL,
    format character varying(1) NOT NULL,
    draw character varying(1) NOT NULL,
    game character varying(3) NOT NULL
);


ALTER TABLE public.tourney_event OWNER TO postgres;

--
-- Name: tourney_event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tourney_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tourney_event_id_seq OWNER TO postgres;

--
-- Name: tourney_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tourney_event_id_seq OWNED BY tourney_event.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tourney_event ALTER COLUMN id SET DEFAULT nextval('tourney_event_id_seq'::regclass);


--
-- Data for Name: tourney_event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tourney_event (id, title, start_at, tournament_id, division, format, draw, game) FROM stdin;
4	Luck of The Draw	2013-06-15 11:15:00-07	10	O	D	L	CR
5	Cricket Doubles	2013-06-15 16:00:00-07	10	M	D	D	CR
6	Cricket Doubles	2013-06-15 16:45:00-07	10	F	D	D	CR
3	Cricket Doubles	2013-06-15 11:00:00-07	10	X	D	L	CR
7	Triples 701	2013-06-16 07:30:00-07	10	M	T	D	701
2	Luck of The Draw	2013-06-14 16:30:00-07	10	F	D	L	CR
1	Luck of The Draw	2013-06-14 16:00:00-07	10	M	D	L	CR
\.


--
-- Name: tourney_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tourney_event_id_seq', 10, true);


--
-- Name: tourney_event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tourney_event
    ADD CONSTRAINT tourney_event_pkey PRIMARY KEY (id);


--
-- Name: tourney_event_tournament_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX tourney_event_tournament_id ON tourney_event USING btree (tournament_id);


--
-- Name: tourney_event_tournament_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tourney_event
    ADD CONSTRAINT tourney_event_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES tourney_tournament(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

