
--consulta iner join

SELECT p.idProdutor, p.nome, COUNT(d.idDocumento) AS total_documentos
FROM Produtor p
LEFT JOIN Documento d ON p.idProdutor = d.Produtor_idProdutor
GROUP BY p.idProdutor, p.nome
HAVING total_documentos > 10;

--consulta sub select
SELECT nome
FROM Produtor
WHERE idProdutor IN (
    SELECT Produtor_idProdutor
    FROM Documento
    WHERE categoria = 1
);


-- Função para calcular a idade baseada na data de nascimento
DELIMITER $$
CREATE FUNCTION calcular_idade(data_nascimento DATE)
RETURNS INT
BEGIN
    DECLARE idade INT;
    SET idade = YEAR(CURDATE()) - YEAR(data_nascimento);
    IF MONTH(CURDATE()) < MONTH(data_nascimento) OR (MONTH(CURDATE()) = MONTH(data_nascimento) AND DAY(CURDATE()) < DAY(data_nascimento)) THEN
        SET idade = idade - 1;
    END IF;
    RETURN idade;
END$$
DELIMITER ;


-- Stored Procedure para inserir um novo produtor
DELIMITER $$
CREATE PROCEDURE inserir_produtor(nome VARCHAR(255), cpf VARCHAR(11), email VARCHAR(255), cnpj VARCHAR(14), razaosocial VARCHAR(255), observacoes VARCHAR(255), status VARCHAR(255))
BEGIN
    INSERT INTO Produtor (nome, cpf, email, cnpj, razaosocial, observacoes, status)
    VALUES (nome, cpf, email, cnpj, razaosocial, observacoes, status);
END$$
DELIMITER ;


-- View para listar produtores com seus documentos
CREATE VIEW vw_produtor_documentos AS
SELECT p.idProdutor, p.nome, d.titulo
FROM Produtor p
LEFT JOIN Documento d ON p.idProdutor = d.Produtor_idProdutor;


-- Trigger para registrar a criação de novos documentos
DELIMITER $$
CREATE TRIGGER trg_documento_insert
AFTER INSERT ON Documento
FOR EACH ROW
BEGIN
    INSERT INTO Log_Documentos (acao, documento_id, data_registro)
    VALUES ('INSERT', NEW.idDocumento, NOW());
END$$
DELIMITER ;





