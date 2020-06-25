--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    user_id integer,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    user_id integer,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    accepted bool
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    user_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);

DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    email text,
    password text,
    registration_time timestamp without time zone
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);


SELECT pg_catalog.setval('answer_id_seq', 2, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00');
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00');
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
