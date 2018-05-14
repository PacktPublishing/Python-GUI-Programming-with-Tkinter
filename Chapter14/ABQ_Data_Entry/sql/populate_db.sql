INSERT INTO lab_techs VALUES
    (4291, 'J Simms'),
    (4319, 'P Taylor'),
    (4478, 'Q Murphy'),
    (5607, 'L Taniff')
    ;

INSERT INTO labs VALUES
    ('A'), ('B'), ('C'), ('D'), ('E');

INSERT INTO plots (SELECT labs.id, plotnums.plot
FROM labs, (SELECT generate_series(1, 20) plot) AS plotnums);

UPDATE plots SET current_seed_sample=
    (CASE WHEN plot % 4 = 1 THEN 'AXM477'
    WHEN plot % 4 = 2 THEN 'AXM478'
    WHEN plot % 4 = 3 THEN 'AXM479'
    WHEN plot % 4 = 0 THEN 'AXM480'
    ELSE '' END)
;
