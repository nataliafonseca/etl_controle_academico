CREATE SCHEMA operational;
CREATE TABLE operational.departamento (
  codigo_departamento SERIAL PRIMARY KEY,
  nome_departamento VARCHAR(300) NOT NULL
);
CREATE TABLE operational.professor (
  matricula_professor SERIAL PRIMARY KEY,
  nome_professor VARCHAR(300) NOT NULL,
  titulacao_professor VARCHAR(20) NOT NULL,
  endereco_professor VARCHAR (500) NOT NULL,
  codigo_departamento INT REFERENCES operational.departamento ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE operational.curso (
  codigo_curso SERIAL PRIMARY KEY,
  descricao_curso VARCHAR(300) NOT NULL,
  creditos_curso INT NOT NULL,
  duracao_curso INT NOT NULL,
  codigo_departamento INT REFERENCES operational.departamento ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE operational.aluno (
  matricula_aluno SERIAL PRIMARY KEY,
  nome_aluno VARCHAR(300) NOT NULL,
  estado_civil_aluno VARCHAR(20) NOT NULL,
  sexo_aluno VARCHAR(2) NOT NULL CHECK (sexo_aluno in ('F', 'M', 'NB')),
  ano_ingresso_aluno INT NOT NULL,
  codigo_curso INT REFERENCES operational.curso ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE operational.disciplina (
  codigo_disciplina SERIAL PRIMARY KEY,
  nome_disciplina VARCHAR(300) NOT NULL,
  creditos_disciplina INT NOT NULL,
  natureza_disciplina VARCHAR(7) NOT NULL CHECK (natureza_disciplina in ('teoria', 'pratica')),
  codigo_curso INT REFERENCES operational.curso ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE operational.turma (
  ano INT NOT NULL,
  periodo INT NOT NULL,
  sala INT NOT NULL,
  PRIMARY KEY (ano, periodo),
  matricula_aluno INT REFERENCES operational.aluno ON DELETE CASCADE ON UPDATE CASCADE,
  matricula_professor INT REFERENCES operational.professor ON DELETE CASCADE ON UPDATE CASCADE,
  codigo_disciplina INT REFERENCES operational.disciplina ON DELETE CASCADE ON UPDATE CASCADE
);