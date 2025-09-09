from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from utils import get_data
app = Flask(__name__)
load_dotenv('.cred')


config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'imoveisdb'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}
def connect_db():
    return None 


@app.route('/imoveis', methods=['GET'])
def imoveis():
    resp, status = get_data()
    return resp, status




if __name__ == "__main__":
    app.run(debug=True)