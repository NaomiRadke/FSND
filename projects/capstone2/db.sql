--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actors; Type: TABLE; Schema: public; Owner: naomiradke
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying NOT NULL,
    age integer NOT NULL,
    gender character varying NOT NULL
);


ALTER TABLE public.actors OWNER TO naomiradke;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: naomiradke
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO naomiradke;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: naomiradke
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: naomiradke
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying NOT NULL,
    release_date timestamp without time zone NOT NULL
);


ALTER TABLE public.movies OWNER TO naomiradke;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: naomiradke
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO naomiradke;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: naomiradke
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: naomiradke
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: naomiradke
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: naomiradke
--

COPY public.actors (id, name, age, gender) FROM stdin;
1	Tweety	15	W
2	Sarah B	44	W
3	Roy Black	14	M
4	Hannah Holy	35	W
5	Jane Austin	45	W
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: naomiradke
--

COPY public.movies (id, title, release_date) FROM stdin;
1	The Mountains	2019-04-04 00:00:00
2	The River	2013-08-03 00:00:00
3	Fun Facts	2020-02-14 00:00:00
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: naomiradke
--

SELECT pg_catalog.setval('public.actors_id_seq', 5, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: naomiradke
--

SELECT pg_catalog.setval('public.movies_id_seq', 3, true);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: naomiradke
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: naomiradke
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

