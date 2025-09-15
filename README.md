# Projeto 2 - API de Imóveis 

API RESTful desenvolvida em Python (Flask) para gerenciamento de imóveis, com suporte a operações CRUD (criação, leitura, atualização e exclusão) e conexão a banco de dados MySQL.

## Deploy na AWS
A API está em produção e pode ser acessada em: [http://54.233.39.212:8000](http://54.233.39.212:8000)

## Tecnologias Utilizadas
- Python 3.9  
- Flask  
- MySQL Connector  
- Pytest (testes automatizados)  
- Gunicorn (servidor WSGI)  
- Amazon EC2 (deploy na nuvem)  

## Endpoints da API
GET /imoveis  
GET /imoveis/<id>  
GET /imoveis/tipo/<tipo>  
GET /imoveis/cidade/<cidade>  
POST /imoveis  
PUT /imoveis/<id>  
DELETE /imoveis/<id>  

### Exemplo de criação de imóvel (POST /imoveis)
```json
{
  "logradouro": "Rua Nova",
  "tipo_logradouro": "Rua",
  "bairro": "Centro",
  "cidade": "São Paulo",
  "cep": "01010-010",
  "tipo": "Apartamento",
  "valor": 450000.00,
  "data_aquisicao": "2024-01-20"
}
🧪 Testes Automatizados
Os testes foram implementados usando Pytest e podem ser executados com:
pytest -v

Como rodar localmente
Clonar o repositório
git clone https://github.com/insper-classroom/20252-progeficaz-projeto2-esc.git
cd 20252-progeficaz-projeto2-esc

Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

Instalar dependências
pip install -r requirements.txt

Criar arquivo .cred na raiz do projeto
DB_HOST=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=imoveisdb
DB_PORT=3306
SSL_CA_PATH=/opt/imoveis-api/ca.pem

Rodar localmente
python servidor.py

