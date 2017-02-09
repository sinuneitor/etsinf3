CREATE TABLE departamento (
    cod_dep CHAR(4) CONSTRAINT dep_pk PRIMARY KEY INITIALLY DEFERRED,
    nombre VARCHAR2(50) CONSTRAINT dep_nnv_nombre NOT NULL,
    telefono CHAR(8),
    director CHAR(9)
);

CREATE TABLE asignatura (
    cod_asg CHAR(5) CONSTRAINT asi_pk PRIMARY KEY INITIALLY DEFERRED,
    nombre VARCHAR2(50) CONSTRAINT asi_nnv_nombre NOT NULL
        CONSTRAINT asi_uni_nombre UNIQUE,
    semestre CHAR(2) CONSTRAINT asi_nnv_semestre NOT NULL
        CONSTRAINT asi_semestre CHECK (semestre IN
            ('1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B')),
    cod_dep CHAR(4) CONSTRAINT asi_nnv_dep NOT NULL
        CONSTRAINT asi_fk_dep REFERENCES departamento(cod_dep) INITIALLY DEFERRED,
    teoria REAL CONSTRAINT asi_nnv_teoria NOT NULL,
    practicas REAL CONSTRAINT asi_nnv_practicas NOT NULL,
    CONSTRAINT asi_teoprac CHECK (teoria >= practicas)
);

CREATE TABLE profesor (
    dni CHAR(9) CONSTRAINT pro_pk PRIMARY KEY INITIALLY DEFERRED,
    nombre VARCHAR2(80) CONSTRAINT pro_vnn_nombre NOT NULL,
    telefono CHAR(8),
    cod_dep CHAR(4) CONSTRAINT pro_nnv_dep NOT NULL
        CONSTRAINT pro_fk_dep REFERENCES departamento(cod_dep) INITIALLY DEFERRED,
    provincia VARCHAR2(25),
    edad INT
);

CREATE TABLE docencia (
    dni CHAR(9) CONSTRAINT doc_fk_pro REFERENCES profesor(dni) INITIALLY DEFERRED,
    cod_asg CHAR(5) CONSTRAINT doc_fk_asi REFERENCES asignatura(cod_asg) INITIALLY DEFERRED,
    gteo INT CONSTRAINT doc_nnv_gteo NOT NULL,
    gpra INT CONSTRAINT doc_nnv_gpra NOT NULL,
    CONSTRAINT doc_pk PRIMARY KEY (dni, cod_asg) INITIALLY DEFERRED
);

ALTER TABLE departamento ADD (
    CONSTRAINT dep_fk_pro FOREIGN KEY (director) REFERENCES profesor(dni) INITIALLY DEFERRED
);

-- Every lecturer must teach at least one subject

CREATE OR REPLACE TRIGGER general_constraint_1_1
AFTER INSERT ON profesor
DECLARE
  howmany NUMBER;
BEGIN
  SELECT COUNT(*) INTO howmany
  FROM profesor
  WHERE dni NOT IN (SELECT dni FROM docencia);
  IF howmany > 0 THEN
    RAISE_APPLICATION_ERROR (-20000, 'All teachers must teach');
  END IF;
END;

CREATE OR REPLACE TRIGGER general_constraint_1_2
AFTER DELETE OR UPDATE OF dni ON docencia
DECLARE
  howmany NUMBER;
BEGIN
  SELECT COUNT(*) INTO howmany
  FROM profesor
  WHERE dni NOT IN (SELECT dni FROM docencia);
  IF howmany > 0 THEN
    RAISE_APPLICATION_ERROR (-20000, 'All teachers must teach');
  END IF;
END;