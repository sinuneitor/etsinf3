DROP TABLE profesor CASCADE CONSTRAINTS;
DROP TABLE asignatura CASCADE CONSTRAINTS;
DROP TABLE docencia CASCADE CONSTRAINTS;
DROP TABLE departamento CASCADE CONSTRAINTS;


----- VALUES TO BE INSERTED IN THE DATABASE ------
INSERT INTO departamento VALUES ('DLA', 'Linguistica Aplicada', '2255', '111');
INSERT INTO departamento VALUES ('DMA', 'Matematica Aplicada', '1256', NULL);
INSERT INTO departamento VALUES ('DSIC', 'Sistemas Informaticos y Computacion', '1242', '453');

INSERT INTO asignatura VALUES ('11545', 'Analisis Matematico', '1A', 'DMA', 4.5, 1.5);
INSERT INTO asignatura VALUES ('11546', 'Algebra', '1B', 'DMA', 4.5, 1.5);
INSERT INTO asignatura VALUES ('11547', 'Matematica Discreta', '1A', 'DMA', 4.5, 1.5);
INSERT INTO asignatura VALUES ('11548', 'Bases de Datos y Sistemas de Informacion',
    '3A', 'DSIC', 4.5, 1.5);

INSERT INTO profesor VALUES ('111', 'Luisa Bos Perez', NULL, 'DMA', 'Alicante', 33);
INSERT INTO profesor VALUES ('123', 'Juana Cerda Perez', '3222', 'DMA', 'Valencia', 50);
INSERT INTO profesor VALUES ('453', 'Elisa Rojo Amando', '7859', 'DSIC', 'Valencia', 26);
INSERT INTO profesor VALUES ('564', 'Pedro Marti Garcia', '3412', 'DMA', 'Castellon', 27);

INSERT INTO docencia VALUES ('111', '11547', 1, 3);
INSERT INTO docencia VALUES ('123', '11545', 0, 2);
INSERT INTO docencia VALUES ('123', '11547', 1, 1);
INSERT INTO docencia VALUES ('453', '11547', 2, 1);
INSERT INTO docencia VALUES ('564', '11545', 2, 2);
------------------ END VALUES ---------------------

CREATE VIEW semestre1 AS
    SELECT *
    FROM asignatura
    WHERE semestre LIKE '1_';
    
SELECT nombre
FROM semestre1
WHERE practicas > 1;