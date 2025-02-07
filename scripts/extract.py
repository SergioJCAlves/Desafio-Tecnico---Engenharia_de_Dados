import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "https://api.openbrewerydb.org/breweries"
API_PARAMS = {'per_page': 50}

def extract_data(**kwargs):
    try:
        response = requests.get(API_URL, params=API_PARAMS)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        
        # Salvar os dados brutos em um arquivo parquet
        df.to_parquet('/tmp/raw_data.parquet')
        
        logger.info(f"Dados extraídos com sucesso. Total de linhas: {len(df)}")
    except Exception as e:
        logger.error(f"Erro ao extrair dados da API: {str(e)}")
        raise

if __name__ == "__main__":
    extract_data()