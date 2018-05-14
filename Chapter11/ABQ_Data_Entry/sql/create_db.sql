-- Lab techs
-- Use employee ID # as primary key
-- Since names can change
-- Names must be unique since they will be displayed
-- In a dropdown
CREATE TABLE lab_techs (
        id SMALLINT PRIMARY KEY,
        name VARCHAR(512) UNIQUE NOT NULL
        );

CREATE TABLE labs (
        id CHAR(1) PRIMARY KEY
        );

CREATE TABLE plots (
        lab_id CHAR(1) NOT NULL REFERENCES labs(id),
        plot SMALLINT NOT NULL,
        current_seed_sample CHAR(6),
        PRIMARY KEY(lab_id, plot),
        CONSTRAINT valid_plot CHECK (plot BETWEEN 1 AND 20)
        );

CREATE TABLE lab_checks(
        date DATE NOT NULL,
        time TIME NOT NULL,
        lab_id CHAR(1) NOT NULL REFERENCES labs(id),
        lab_tech_id SMALLINT NOT NULL REFERENCES lab_techs(id),
        PRIMARY KEY(date, time, lab_id)
        );

CREATE TABLE plot_checks(
        date DATE NOT NULL,
        time TIME NOT NULL,
        lab_id CHAR(1) NOT NULL REFERENCES labs(id),
        plot SMALLINT NOT NULL,
        seed_sample CHAR(6) NOT NULL,
        humidity NUMERIC(4, 2) CHECK (humidity BETWEEN 0.5 AND 52.0),
        light NUMERIC(5, 2) CHECK (light BETWEEN 0 AND 100),
        temperature NUMERIC(4, 2) CHECK (temperature BETWEEN 4 AND 40),
        equipment_fault BOOLEAN NOT NULL,
        blossoms SMALLINT NOT NULL CHECK (blossoms BETWEEN 0 AND 1000),
        plants SMALLINT NOT NULL CHECK (plants BETWEEN 0 AND 20),
        fruit SMALLINT NOT NULL CHECK (fruit BETWEEN 0 AND 1000),
        max_height NUMERIC(6, 2) NOT NULL CHECK (max_height BETWEEN 0 AND 1000),
        min_height NUMERIC(6, 2) NOT NULL CHECK (min_height BETWEEN 0 AND 1000),
        median_height NUMERIC(6, 2)
            NOT NULL CHECK
            (median_height BETWEEN min_height AND max_height),
        notes TEXT,
        PRIMARY KEY(date, time, lab_id, plot),
        FOREIGN KEY(lab_id, date, time)
            REFERENCES lab_checks(lab_id, date, time),
        FOREIGN KEY(lab_id, plot) REFERENCES plots(lab_id, plot)
        );

CREATE VIEW data_record_view AS (
    SELECT pc.date AS "Date",
        to_char(pc.time, 'FMHH24:MI') AS "Time",
        lt.name AS "Technician",
        pc.lab_id AS "Lab",
        pc.plot AS "Plot",
        pc.seed_sample AS "Seed sample",
        pc.humidity AS "Humidity",
        pc.light AS "Light",
        pc.temperature AS "Temperature",
        pc.plants AS "Plants",
        pc.blossoms AS "Blossoms",
        pc.fruit AS "Fruit",
        pc.max_height AS "Max Height",
        pc.min_height AS "Min Height",
        pc.median_height AS "Median Height",
        pc.notes AS "Notes"
    FROM plot_checks AS pc
        JOIN lab_checks AS lc
            ON pc.lab_id = lc.lab_id
            AND pc.date = lc.date
            AND pc.time = lc.time
        JOIN lab_techs AS lt
            ON lc.lab_tech_id = lt.id
        );
