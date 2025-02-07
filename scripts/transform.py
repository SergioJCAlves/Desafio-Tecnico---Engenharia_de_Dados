import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform_data(**kwargs):
    try:
        # Ler os dados brutos
        df = pd.read_parquet('/tmp/raw_data.parquet')
        
        # Transformações para a camada Silver
        silver_df = df[['name', 'brewery_type', 'city', 'state', 'country']]
        silver_df.columns = ['nome', 'tipo', 'cidade', 'estado', 'pais']
        silver_df['tipo'] = silver_df['tipo'].str.lower()
        
        # Salvar os dados da camada Silver
        silver_df.to_parquet('/tmp/silver_data.parquet')
        
        # Transformações para a camada Gold
        gold_df = silver_df.groupby(['tipo', 'pais']).size().reset_index(name='quantidade_cervejarias')
        
        # Salvar os dados da camada Gold
        gold_df.to_parquet('/tmp/gold_data.parquet')
        
        logger.info("Dados transformados com sucesso")
    except Exception as e:
        logger.error(f"Erro na transformação dos dados: {str(e)}")
        raise

if __name__ == "__main__":
    transform_data()