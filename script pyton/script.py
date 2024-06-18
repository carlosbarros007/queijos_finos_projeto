import mysql.connector
from faker import Faker
from datetime import datetime

# Função para inserir dados na tabela Produtor
def insert_produtor(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        nome = faker.name()
        cpf = faker.unique.random_number(digits=11)
        email = faker.email()
        cnpj = faker.unique.random_number(digits=14)
        razaosocial = faker.company()
        observacoes = faker.text(max_nb_chars=255)  # Limita a 255 caracteres
        status = faker.random_element(elements=('ativo', 'inativo'))
        query = "INSERT INTO Produtor (nome, cpf, email, cnpj, razaosocial, observacoes, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, cpf, email, cnpj, razaosocial, observacoes, status))
    print("Dados inseridos na tabela Produtor.")

# Função para inserir dados na tabela Documento
def insert_documento(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        titulo = faker.sentence()
        arquivo = faker.file_name()
        data = faker.date_this_decade()
        data_sistema = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        categoria = faker.random_number(digits=1)
        # Seleciona um ID de produtor existente na tabela Produtor
        cursor.execute("SELECT idProdutor FROM Produtor ORDER BY RAND() LIMIT 1")
        produtor_id = cursor.fetchone()[0]
        query = "INSERT INTO Documento (titulo, arquivo, data, data_sistema, categoria, Produtor_idProdutor) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (titulo, arquivo, data, data_sistema, categoria, produtor_id))
    print("Dados inseridos na tabela Documento.")

# Função para inserir dados na tabela Endereco
def insert_endereco(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        cep = faker.zipcode()
        rua = faker.street_name()
        numero = faker.building_number()
        bairro = faker.city()
        latitude = faker.latitude()
        longitude = faker.longitude()
        # Seleciona um ID de produtor existente na tabela Produtor
        cursor.execute("SELECT idProdutor FROM Produtor ORDER BY RAND() LIMIT 1")
        produtor_id = cursor.fetchone()[0]
        query = "INSERT INTO Endereco (cep, rua, numero, bairro, latitude, longitude, Produtor_idProdutor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (cep, rua, numero, bairro, latitude, longitude, produtor_id))
    print("Dados inseridos na tabela Endereco.")

# Função para inserir dados na tabela Usuario
def insert_usuario(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        email = faker.email()
        senha = faker.password()
        permissao = faker.random_number(digits=1)
        query = "INSERT INTO Usuario (email, senha, permissao) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, senha, permissao))
    print("Dados inseridos na tabela Usuario.")

# Função para inserir dados na tabela Tecnologia
def insert_tecnologia(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        nome = faker.word()
        observacao = faker.text(max_nb_chars=255)  # Limita a 255 caracteres
        query = "INSERT INTO Tecnologia (nome, observacao) VALUES (%s, %s)"
        cursor.execute(query, (nome, observacao))
    print("Dados inseridos na tabela Tecnologia.")

# Função para inserir dados na tabela Transferencia
def insert_transferencia(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        data_inicio = faker.date_this_decade()
        data_conclusao = faker.date_between(start_date=data_inicio)
        # Seleciona um ID de produtor e de tecnologia existentes nas tabelas relacionadas
        cursor.execute("SELECT idProdutor FROM Produtor ORDER BY RAND() LIMIT 1")
        produtor_id = cursor.fetchone()[0]
        cursor.execute("SELECT idTecnologia FROM Tecnologia ORDER BY RAND() LIMIT 1")
        tecnologia_id = cursor.fetchone()[0]
        query = "INSERT INTO Transferencia (data_inicio, data_conclusao, Produtor_idProdutor, Tecnologia_idTecnologia) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data_inicio, data_conclusao, produtor_id, tecnologia_id))
    print("Dados inseridos na tabela Transferencia.")

# Função para inserir dados na tabela Certificado
def insert_certificado(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        data_emissao = faker.date_this_decade()
        orgao_emissor = faker.company()
        # Seleciona um ID de produtor existente na tabela Produtor
        cursor.execute("SELECT idProdutor FROM Produtor ORDER BY RAND() LIMIT 1")
        produtor_id = cursor.fetchone()[0]
        query = "INSERT INTO Certificado (data_emissao, orgao_emissor, Produtor_idProdutor) VALUES (%s, %s, %s)"
        cursor.execute(query, (data_emissao, orgao_emissor, produtor_id))
    print("Dados inseridos na tabela Certificado.")

# Função para inserir dados na tabela Telefone
def insert_telefone(cursor):
    for _ in range(3):  # Insere 3 registros fictícios
        telefone = faker.phone_number()
        # Seleciona um ID de produtor existente na tabela Produtor
        cursor.execute("SELECT idProdutor FROM Produtor ORDER BY RAND() LIMIT 1")
        produtor_id = cursor.fetchone()[0]
        query = "INSERT INTO Telefone (telefone, Produtor_idProdutor) VALUES (%s, %s)"
        cursor.execute(query, (telefone, produtor_id))
    print("Dados inseridos na tabela Telefone.")

# Conecta ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",  # ou o endereço IP do servidor MySQL
    port="3306",       # porta padrão do MySQL
    user="root",
    password="nova_senha",
    database="mydb"
)

# Verifica se a conexão foi bem-sucedida
if conn.is_connected():
    print("Conexão bem-sucedida.")
else:
    print("Falha na conexão.")

# Cria um objeto Faker para gerar dados fictícios
faker = Faker()

# Lista de funções de inserção para serem executadas de forma intercalada
insert_functions = [
    insert_produtor,
    insert_documento,
    insert_endereco,
    insert_usuario,
    insert_tecnologia,
    insert_transferencia,
    insert_certificado,
    insert_telefone
]

# Cria um cursor para executar as consultas SQL
cursor = conn.cursor()

# Loop infinito para inserir dados de forma intercalada
while True:
    for insert_func in insert_functions:
        insert_func(cursor)
        conn.commit()

# Fechamento do cursor e da conexão
cursor.close()
conn.close()
