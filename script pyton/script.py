import mysql.connector
from faker import Faker
from datetime import datetime

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

# Função para inserir dados na tabela Produtor
def insert_produtor(cursor):
    for _ in range(10000):  # Insere 10 registros fictícios
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
    for _ in range(10000):  # Insere 10 registros fictícios
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
    for _ in range(10000):  # Insere 10 registros fictícios
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

# Cria um cursor para executar as consultas SQL
cursor = conn.cursor()

# Chama as funções para inserir dados em cada tabela
insert_produtor(cursor)
insert_documento(cursor)
insert_endereco(cursor)

# Commit das alterações e fechamento do cursor e da conexão
conn.commit()
cursor.close()
conn.close()
