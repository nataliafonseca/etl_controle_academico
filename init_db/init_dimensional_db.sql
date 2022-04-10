CREATE SCHEMA dimensional;
CREATE TABLE dimensional.dm_aluno (
  id_aluno INT PRIMARY KEY,
  matricula_aluno INT NOT NULL,
  nome_aluno VARCHAR(300) NOT NULL
);
CREATE TABLE dimensional.dm_departamento (
  id_departamento INT PRIMARY KEY,
  codigo_departamento INT NOT NULL,
  nome_departamento VARCHAR(300) NOT NULL
);
CREATE TABLE dimensional.dm_disciplina (
  id_disciplina INT PRIMARY KEY,
  codigo_disciplina INT NOT NULL,
  nome_disciplina VARCHAR(300) NOT NULL,
  creditos_disciplina INT NOT NULL,
  natureza_disciplina VARCHAR(7) NOT NULL CHECK (natureza_disciplina in ('teoria', 'pratica'))
);
CREATE TABLE dimensional.dm_tempo (
  id_tempo INT PRIMARY KEY,
  ano INT NOT NULL,
  semestre INT NOT NULL,
  periodo CHAR(6) NOT NULL
);
CREATE TABLE dimensional.ft_professor (
  id_aluno INT REFERENCES dimensional.dm_aluno ON DELETE CASCADE ON UPDATE CASCADE,
  id_departamento INT REFERENCES dimensional.dm_departamento ON DELETE CASCADE ON UPDATE CASCADE,
  id_disciplina INT REFERENCES dimensional.dm_disciplina ON DELETE CASCADE ON UPDATE CASCADE,
  id_tempo INT REFERENCES dimensional.dm_tempo ON DELETE CASCADE ON UPDATE CASCADE,
  produtividade FLOAT NOT NULL,
  PRIMARY KEY (
    id_aluno,
    id_departamento,
    id_disciplina,
    id_tempo
  )
);