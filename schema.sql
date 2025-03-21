-- This file should contain all code required to create & seed database tables.
DROP TABLE IF EXISTS request_interaction;
DROP TABLE IF EXISTS rating_interaction;
DROP TABLE IF EXISTS exhibition;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS floor;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS rating;

CREATE TABLE department (
    department_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO department (department_name) VALUES 
('Ecology'),
('Entomology'),
('Geology'),
('Paleontology'),
('Zoology');

CREATE TABLE floor (
    floor_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    floor_name VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO floor (floor_name) VALUES
('1'),
('2'),
('3'),
('vault');

CREATE TABLE exhibition (
    exhibition_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    exhibition_name VARCHAR(100) UNIQUE NOT NULL,
    exhibition_description TEXT,
    department_id SMALLINT,
    floor_id SMALLINT,
    exhibition_start_date DATE DEFAULT CURRENT_DATE CHECK (exhibition_start_date <= CURRENT_DATE),
    public_id TEXT,
    FOREIGN KEY(floor_id) REFERENCES floor(floor_id),
    FOREIGN KEY(department_id) REFERENCES department(department_id)
);

INSERT INTO exhibition (exhibition_name, exhibition_description, department_id, floor_id, exhibition_start_date, public_id) VALUES
('Adaptation', 'How insect evolution has kept pace with an industrialised world', 2, 4, '2019/07/01', 'EXH_01'),
('The Crenshaw Collection','An exhibition of 18th Century watercolours, mostly focused on South American wildlife.',5, 2, '2021/03/03', 'EXH_02'),
('Cetacean Sensations','Whales: from ancient myth to critically endangered.',5, 1, '2019/07/01', 'EXH_03'),
('Our Polluted World','A hard-hitting exploration of humanity''s impact on the environment.',1, 3, '2021/05/12', 'EXH_04'),
('Thunder Lizards','How new research is making scientists rethink what dinosaurs really looked like.',4, 1, '2023/02/01', 'EXH_05'),
('Measureless to Man','An immersive 3D experience: delve deep into a previously-inaccessible cave system.', 3, 1, '2021/08/23', 'EXH_00');

CREATE TABLE request (
    request_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    request_value SMALLINT,
    request_description VARCHAR(100)
);

INSERT INTO request (request_value, request_description) VALUES
(1, 'emergency'),
(0, 'assistance');


CREATE TABLE rating (
    rating_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    rating_value SMALLINT,
    rating_description VARCHAR(100)
);

INSERT INTO rating (rating_value, rating_description) VALUES
(1, 'bad'),
(2, 'neutral'),
(3, 'good'),
(4, 'amazing'),
(0, 'terrible');

CREATE TABLE request_interaction (
    request_interaction_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    exhibition_id SMALLINT,
    request_id SMALLINT,
    event_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY(request_id) REFERENCES request(request_id)

);

CREATE TABLE rating_interaction (
    rating_interaction_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    exhibition_id SMALLINT,
    rating_id SMALLINT,
    event_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY(rating_id) REFERENCES rating(rating_id)

);