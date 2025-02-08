# Projeto ETL de Cervejarias

Este projeto implementa um pipeline de ETL (Extract, Transform, Load) para processar dados de cervejarias da Open Brewery DB API, seguindo uma arquitetura de medalhão com três camadas: dados brutos, dados tratados particionados por localização e uma camada analítica agregada.

## Arquitetura do projeto

```
project/
├── dags/
│   └── cervejarias_etl_dag.py
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── Dockerfile
├── docker-compose.yaml
└── README.md
```

## Escolhas de Design e Compensações

### Ferramenta de Orquestração
- **Escolha**: Apache Airflow
- **Justificativa**: O Airflow foi escolhido devido à sua robustez na orquestração de workflows complexos, capacidade de agendamento flexível e facilidade de monitoramento de tarefas.
- **Compensação**: Embora o Airflow tenha uma curva de aprendizado mais íngreme comparado a algumas alternativas, sua flexibilidade e recursos avançados compensam esse desafio inicial.

### Linguagem e Bibliotecas
- **Linguagem**: Python
- **Bibliotecas principais**: 
  - `requests` para chamadas à API
  - `pandas` para manipulação de dados
  - `pyarrow` para trabalhar com arquivos Parquet
- **Justificativa**: Python oferece uma ampla gama de bibliotecas para processamento de dados e integração com várias ferramentas de Big Data.

### Arquitetura de Data Lake
- **Estrutura**: Arquitetura de medalhão (Bronze, Silver, Gold)
- **Formatos de arquivo**:
  - Bronze: JSON (dados brutos da API)
  - Silver: Parquet (dados transformados e particionados)
  - Gold: CSV (dados agregados para análise)
- **Justificativa**: Esta estrutura permite uma clara separação entre dados brutos, processados e analíticos, facilitando a governança de dados e otimizando o desempenho das consultas.

### Containerização
- **Tecnologia**: Docker e Docker Compose
- **Justificativa**: Containerização garante consistência entre ambientes de desenvolvimento e produção, além de facilitar a implantação e escalabilidade.

## Como Executar a Aplicação

1. **Pré-requisitos**:
   - Docker e Docker Compose instalados em sua máquina

2. **Configuração**:
   - Clone o repositório:
     ```
     git clone https://github.com/SergioJCAlves/Desafio-Tecnico---Engenharia_de_Dados/
     cd Desafio-Tecnico---Engenharia_de_Dados
     ```
   - (Se aplicável) Configure as variáveis de ambiente no arquivo `.env`

3. **Inicialização**:

    - Crie os containers Docker:
     ```

     docker-compose build
     
     ```
   - Aguarde a finalização

   - Altere as credenciais docker:
     ```

     docker-compose run airflow-webserver airflow users create --username admin --firstname 
     Admin --lastname User --role Admin --email admin@example.com --password admin
     
     ```
   - Aguarde a finalização da instalação


   - Inicie os containers Docker:

     ```
     docker-compose up -d
     ```
     
   - Aguarde alguns minutos para que todos os serviços inicializem completamente

5. **Execução do Pipeline**:
   - Acesse a interface web do Airflow em `http://localhost:8080`
   - Use as credenciais padrão (geralmente airflow/airflow)
   - Localize o DAG "cervejarias_etl" e ative-o
   - Dispare uma execução manual do DAG ou aguarde o agendamento automático

6. **Verificação dos Resultados**:
   - Os dados processados estarão disponíveis nos seguintes caminhos dentro do container:
     - Bronze: `/opt/airflow/data/bronze/breweries_raw.json`
     - Silver: `/opt/airflow/data/silver/breweries.parquet`
     - Gold: `/opt/airflow/data/gold/breweries_aggregated.csv`
   - Para visualizar os dados, use os comandos:
     ```
     docker-compose exec airflow-worker head -n 20 /opt/airflow/data/bronze/breweries_raw.json
     docker-compose exec airflow-worker parquet-tools show /opt/airflow/data/silver/breweries.parquet | head -n 20
     docker-compose exec airflow-worker cat /opt/airflow/data/gold/breweries_aggregated.csv
     ```

7. **Encerrando a Aplicação**:
   - Para parar e remover os containers:
     ```
     docker-compose down
     ```

## Monitoramento e Alertas

O monitoramento é realizado através da interface web do Airflow, que fornece visualizações detalhadas do status de cada tarefa e do DAG como um todo. Para alertas, configuramos notificações por e-mail em caso de falhas nas tarefas críticas do pipeline.

## Tratamento de Erros

O pipeline inclui tratamento de erros para lidar com falhas na API, problemas de conexão e inconsistências nos dados. Logs detalhados são gerados em cada etapa para facilitar a identificação e resolução de problemas.

## Considerações de Segurança

- As credenciais e chaves sensíveis são armazenadas como variáveis de ambiente e não são expostas no código-fonte.
- O acesso à interface web do Airflow é protegido por autenticação.

Para quaisquer dúvidas ou sugestões, por favor, abra uma issue neste repositório ou me ligue.
