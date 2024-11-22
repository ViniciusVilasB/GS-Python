import random
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time
import logging
import os

#####################################################################################################

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Variáveis de ambiente
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "banco_de_consumo")

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    colecao = db['consumo_de_energia']
    logging.info("Conexão ao MongoDB bem-sucedida.")
except Exception as e:
    logging.error("Erro ao conectar ao banco de dados:", exc_info=True)
    exit()

#####################################################################################################

def criar_consumo_aleatorio():
    """
    Gera um consumo de energia aleatório e insere no banco de dados MongoDB.

    O consumo é gerado no intervalo de 0 a 500 kWh com duas casas decimais.
    """
    try:
        consumo_kwh = round(random.uniform(0, 500), 2)
        nome_edificio = "Edificio_Vilas_Boas"
        data_registro = datetime.now()

        documento = {
            "nome_edificio": nome_edificio,
            "consumo_kwh": consumo_kwh,
            "data_registro": data_registro
        }

        colecao.insert_one(documento)
        logging.info(f"Documento inserido: {documento}")
    except Exception as e:
        logging.error("Erro ao criar consumo aleatório:", exc_info=True)


def criar_grafico_consumo():
    """
    Gera um gráfico dos últimos 10 registros de consumo no banco de dados.
    O gráfico é exibido na tela e salvo como um arquivo PNG.
    """
    try:
        ultimos_dados = colecao.find().sort("data_registro", -1).limit(10)

        datas = []
        consumos = []

        for dado in ultimos_dados:
            datas.append(dado["data_registro"])
            consumos.append(dado["consumo_kwh"])

        if not datas:
            logging.warning("Nenhum dado encontrado para criar o gráfico.")
            return

        datas = pd.to_datetime(datas)

        plt.figure(figsize=(10, 6))
        plt.plot(datas, consumos, marker='o', linestyle='-', color='b', label='Consumo (kWh)')

        plt.title('Consumo de Energia nos Últimos 10 Registros', fontsize=16)
        plt.xlabel('Data de Registro', fontsize=12)
        plt.ylabel('Consumo de Energia (kWh)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()

        plt.savefig("grafico_consumo.png", dpi=300)
        logging.info("Gráfico salvo como 'grafico_consumo.png'")
        plt.show()
    except Exception as e:
        logging.error("Erro ao criar gráfico de consumo:", exc_info=True)


def inserir_consumo_se_vazio(num_registros=10, intervalo=1):
    """
    Insere dados aleatórios de consumo se a coleção estiver vazia.

    Parameters:
        num_registros (int): Quantidade de registros a serem inseridos.
        intervalo (int): Intervalo em segundos entre as inserções.
    """
    try:
        if colecao.count_documents({}) == 0:
            logging.info("Coleção vazia. Inserindo dados aleatórios.")
            for _ in range(num_registros):
                criar_consumo_aleatorio()
                time.sleep(intervalo)
            logging.info(f"{num_registros} documentos inseridos.")
        else:
            logging.info("A coleção já contém documentos.")
    except Exception as e:
        logging.error("Erro ao inserir dados aleatórios:", exc_info=True)

#####################################################################################################

def main():
    """
    Função principal para executar o script de forma integrada.
    """
    inserir_consumo_se_vazio()
    criar_consumo_aleatorio()
    criar_grafico_consumo()


if __name__ == "__main__":
    main()
