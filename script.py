import sqlalchemy
import pandas as pd

# 1. Extract

db_connection = sqlalchemy.create_engine(
    'postgresql+pg8000://postgres:123456@localhost:5433/academicodb',
    client_encoding='utf8',
)

departamento_df = pd.read_sql(
    'SELECT * FROM operational.departamento', db_connection
)
departamento_df

professor_df = pd.read_sql(
    'SELECT * FROM operational.professor', db_connection
)
professor_df

curso_df = pd.read_sql('SELECT * FROM operational.curso', db_connection)
curso_df

aluno_df = pd.read_sql('SELECT * FROM operational.aluno', db_connection)
aluno_df

disciplina_df = pd.read_sql(
    'SELECT * FROM operational.disciplina', db_connection
)
disciplina_df

turma_df = pd.read_sql('SELECT * FROM operational.turma', db_connection)
turma_df

# 2. Transform

dm_aluno_df = aluno_df.drop(
    columns=[
        'estado_civil_aluno',
        'sexo_aluno',
        'ano_ingresso_aluno',
        'codigo_curso',
    ]
)
dm_aluno_df['id_aluno'] = 'matricula_aluno'
dm_aluno_df

dm_departamento_df = departamento_df.copy()
dm_departamento_df['id_departamento'] = 'codigo_departamento'
dm_departamento_df

dm_disciplina_df = disciplina_df.drop(columns=['codigo_curso'])
dm_disciplina_df['id_disciplina'] = 'codigo_disciplina'
dm_disciplina_df

dm_tempo_df = pd.DataFrame()

dm_tempo_df['ano'] = turma_df['ano']
dm_tempo_df['semestre'] = turma_df['periodo']

dm_tempo_df['periodo'] = (
    dm_tempo_df['ano'].astype(str) + '/' + dm_tempo_df['semestre'].astype(str)
)

dm_tempo_df['id_tempo'] = (
    dm_tempo_df['ano'].astype(str) + dm_tempo_df['semestre'].astype(str)
).astype(int)

dm_tempo_df.drop_duplicates(inplace=True)
dm_tempo_df

ft_professor_df = pd.merge(
    left=turma_df, right=professor_df, how='left', on='matricula_professor'
)
ft_professor_df.rename(
    columns={
        'matricula_aluno': 'id_aluno',
        'codigo_departamento': 'id_departamento',
        'codigo_disciplina': 'id_disciplina',
    },
    inplace=True,
)
ft_professor_df['id_tempo'] = (
    ft_professor_df['ano'].astype(str) + ft_professor_df['periodo'].astype(str)
).astype(int)
ft_professor_df.drop(
    columns=[
        'ano',
        'periodo',
        'sala',
        'matricula_professor',
        'nome_professor',
        'titulacao_professor',
        'endereco_professor',
    ],
    inplace=True,
)
ft_professor_df

aux_df = pd.DataFrame()
aux_df['id_tempo'] = ft_professor_df['id_tempo']
aux_df['id_aluno'] = ft_professor_df['id_aluno']
aux_df = aux_df.groupby(['id_tempo'])['id_aluno'].agg('sum')
aux_df


def get_produtividade(periodos):
    lista = []
    for periodo in periodos:
        total_alunos = aux_df[periodo]
        lista.append(total_alunos)
    return lista


ft_professor_df['produtividade'] = get_produtividade(
    ft_professor_df['id_tempo']
)

ft_professor_df

# 3. Load

# Função para calculo do chunksize
def get_chunksize(table_columns):
    cs = 2097 // len(table_columns)
    cs = 1000 if cs > 1000 else cs
    return cs


dm_aluno_df.to_sql(
    name='dm_aluno',
    schema='dimensional',
    con=db_connection,
    index=False,
    if_exists='append',
    chunksize=get_chunksize(dm_aluno_df.columns),
)

dm_disciplina_df.to_sql(
    name='dm_disciplina',
    schema='dimensional',
    con=db_connection,
    index=False,
    if_exists='append',
    chunksize=get_chunksize(dm_disciplina_df.columns),
)

dm_departamento_df.to_sql(
    name='dm_departamento',
    schema='dimensional',
    con=db_connection,
    index=False,
    if_exists='append',
    chunksize=get_chunksize(dm_departamento_df.columns),
)

dm_tempo_df.to_sql(
    name='dm_tempo',
    schema='dimensional',
    con=db_connection,
    index=False,
    if_exists='append',
    chunksize=get_chunksize(dm_tempo_df.columns),
)

ft_professor_df.to_sql(
    name='ft_professor',
    schema='dimensional',
    con=db_connection,
    index=False,
    if_exists='append',
    chunksize=get_chunksize(ft_professor_df.columns),
)
