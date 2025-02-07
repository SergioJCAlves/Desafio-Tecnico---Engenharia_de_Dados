from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import logging
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Defina as configurações padrão para o DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Função para garantir que os diretórios existam
def ensure_directories():
    for path in ['/opt/airflow/data/bronze', '/opt/airflow/data/silver', '/opt/airflow/data/gold']:
        os.makedirs(path, exist_ok=True)

# Função para extrair dados da API
def extract_brewery_data(**kwargs):
    logging.info("Iniciando extração de dados das cervejarias")
    ensure_directories()
    
    base_url = "https://api.openbrewerydb.org/breweries"
    all_breweries = []
    page = 1
    
    try:
        while True:
            logging.info(f"Buscando página {page}")
            response = requests.get(f"{base_url}?page={page}&per_page=50")
            response.raise_for_status()
            breweries = response.json()
            
            if not breweries:
                break
            
            all_breweries.extend(breweries)
            page += 1

        logging.info(f"Total de cervejarias extraídas: {len(all_breweries)}")

        # Salvar os dados brutos (camada Bronze)
        bronze_path = '/opt/airflow/data/bronze/breweries_raw.json'
        with open(bronze_path, 'w') as f:
            json.dump(all_breweries, f)
        
        logging.info(f"Dados brutos salvos em {bronze_path}")
        return len(all_breweries)
    except Exception as e:
        logging.error(f"Erro durante a extração: {str(e)}")
        raise

# Função para transformar os dados
def transform_brewery_data(**kwargs):
    logging.info("Iniciando transformação dos dados")
    
    try:
        # Ler os dados brutos
        with open('/opt/airflow/data/bronze/breweries_raw.json', 'r') as f:
            breweries = json.load(f)
        
        # Transformar os dados
        df = pd.DataFrame(breweries)
        
        # Exemplo de transformação: converter para lowercase e remover espaços
        df['state'] = df['state'].str.lower().str.replace(' ', '_')
        
        # Salvar os dados transformados (camada Prata)
        silver_path = '/opt/airflow/data/silver/breweries.parquet'
        df.to_parquet(silver_path, index=False)
        
        logging.info(f"Dados transformados salvos em {silver_path}")
        return df.shape[0]
    except Exception as e:
        logging.error(f"Erro durante a transformação: {str(e)}")
        raise

# Função para carregar os dados
def load_brewery_data(**kwargs):
    logging.info("Iniciando carregamento dos dados")
    
    try:
        # Ler os dados transformados
        df = pd.read_parquet('/opt/airflow/data/silver/breweries.parquet')
        
        # Agregar os dados
        agg_data = df.groupby(['state', 'brewery_type']).size().reset_index(name='count')
        
        # Salvar os dados agregados (camada Ouro)
        gold_path = '/opt/airflow/data/gold/breweries_aggregated.csv'
        agg_data.to_csv(gold_path, index=False)
        
        logging.info(f"Dados agregados salvos em {gold_path}")
        return agg_data.shape[0]
    except Exception as e:
        logging.error(f"Erro durante o carregamento: {str(e)}")
        raise

# Definir o DAG
with DAG('cervejarias_etl', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:

    extract_task = PythonOperator(
        task_id='extract_brewery_data',
        python_callable=extract_brewery_data,
    )

    transform_task = PythonOperator(
        task_id='transform_brewery_data',
        python_callable=transform_brewery_data,
    )

    load_task = PythonOperator(
        task_id='load_brewery_data',
        python_callable=load_brewery_data,
    )

    # Definir a ordem das tarefas
    extract_task >> transform_task >> load_task