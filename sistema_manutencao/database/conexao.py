import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv() #carrega automaticamente as variaveis existentes no .env

class Conexao:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT", "3306")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.ssl_ca = os.getenv("DB_SSL_CA")  # caminho do certificado da Aiven (ca.pem)

        argumentos_conexao = {
            "host": self.host,
            "port": int(self.port),
            "database": self.database,
            "user": self.user,
            "password": self.password,
        }

        # Aiven exige conexão criptografada. Se o caminho do certificado
        # estiver configurado no .env, a conexão usa SSL.
        if self.ssl_ca:
            argumentos_conexao["ssl_ca"] = self.ssl_ca
            argumentos_conexao["ssl_verify_cert"] = True

        self.conexao = mysql.connector.connect(**argumentos_conexao)
        self.cursor = self.conexao.cursor()

    def commit(self):
        self.conexao.commit()
    def rollback(self):
        self.conexao.rollback()
    def fechar(self):
        self.cursor.close()
        self.conexao.close()
