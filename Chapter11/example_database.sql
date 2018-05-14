-- Create and insert
CREATE TABLE musicians (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        born DATE,
        died DATE CHECK (died > born)
        );

INSERT INTO musicians (name, born, died) VALUES
    ('Robert Fripp', '1946-05-16', NULL),
    ('Keith Emerson', '1944-11-02', '2016-03-11'),
    ('Greg Lake', '1947-11-10', '2016-12-7'),
    ('Bill Bruford', '1949-05-17', NULL),
    ('David Gilmour', '1946-03-06', NULL)
;

CREATE TABLE instruments (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        );

INSERT INTO instruments (name) VALUES
    ('bass'), ('drums'), ('guitar'), ('keyboards');

ALTER TABLE musicians ADD COLUMN main_instrument INT REFERENCES instruments(id);

-- Select data

SELECT name FROM musicians;

SELECT * FROM musicians;

SELECT name FROM musicians WHERE died IS NULL;

SELECT name FROM musicians WHERE born < '1945-01-01' AND died IS NULL;

SELECT name, age(born), (died - born)/365 AS "age at death"
FROM musicians ORDER BY born DESC;


-- Update data
UPDATE musicians SET main_instrument=3 WHERE id=1;
UPDATE musicians SET main_instrument=2 WHERE name='Bill Bruford';
UPDATE musicians SET main_instrument=4, name='Keith Noel Emerson' WHERE name LIKE 'Keith%';
UPDATE musicians SET main_instrument=1 WHERE LOWER(name) LIKE '%lake';

-- subqueries
UPDATE musicians SET main_instrument=(SELECT id FROM instruments WHERE name='guitar') WHERE name IN ('Robert Fripp', 'David Gilmour');
SELECT name FROM musicians WHERE main_instrument IN (SELECT id FROM instruments WHERE name like '%r%');

SELECT name FROM (SELECT * FROM musicians WHERE died IS NULL) AS living_musicians;

-- Joins and aggregates

SELECT musicians.name, instruments.name as main_instrument
FROM musicians
    JOIN instruments on musicians.main_instrument = instrument.id;

SELECT instruments.name AS instrument, musicians.name as musician
FROM instruments
    JOIN musicians on musicians.main_instrument = instruments.id;

SELECT instruments.name AS instrument, count(musicians.id) as musicians
FROM instruments
    JOIN musicians on musicians.main_instrument = instruments.id
GROUP BY instruments.name;


CREATE TABLE bands (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        );
INSERT INTO bands(name) VALUES ('ABWH'), ('ELP'), ('King Crimson'), ('Pink Floyd'), ('Yes');

CREATE TABLE musicians_bands (
        musician_id INT REFERENCES musicians(id),
        band_id INT REFERENCES bands(id),
        PRIMARY KEY (musician_id, band_id)
        );

INSERT INTO musicians_bands(musician_id, band_id)
VALUES (1, 3), (2, 2), (3, 2), (3, 3), (4, 1), (4, 2), (4, 5), (5,4);

SELECT musicians.name, array_agg(bands.name) as bands
FROM musicians
    JOIN musicians_bands on musicians.id = musicians_bands.musician_id
    JOIN bands on bands.id = musicians_bands.band_id
GROUP BY musicians.name
ORDER BY musicians.name ASC
;
