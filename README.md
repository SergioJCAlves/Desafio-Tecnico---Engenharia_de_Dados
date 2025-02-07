# Projeto ETL de Cervejarias

Este projeto implementa um pipeline de ETL (Extract, Transform, Load) para processar dados de cervejarias da Open Brewery DB API, seguindo uma arquitetura de medalhão com três camadas: dados brutos, dados tratados particionados por localização e uma camada analítica agregada.


## Estrutura do Projeto

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

## Configuração e Execução

1. **Pré-requisitos**:
   - Docker e Docker Compose instalados em sua máquina

2. **Configuração**:
   - Clone o repositório:
     ```
     Faça o download do repositório
     
     ```

3. **Inicialização**:
   - Inicie os containers Docker:
     ```
     docker-compose up -d
     ```
   - Aguarde alguns minutos para que todos os serviços inicializem completamente

4. **Execução do Pipeline**:
   - Acesse a interface web do Airflow em `http://localhost:8080`
   - Use as credenciais padrão (geralmente airflow/airflow)
   - Localize o DAG "cervejarias_etl" e ative-o
   - Dispare uma execução manual do DAG ou aguarde o agendamento automático

5. **Verificação dos Resultados**:
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

6. **Encerrando a Aplicação**:
   - Para parar e remover os containers:
     ```
     docker-compose down
     ```

## Camadas de Dados

### Bronze (Raw Data)
- `breweries_raw.json`: Dados brutos da API de cervejarias

### Silver (Treated Data)
- `breweries.parquet`: Dados tratados e particionados por localização

### Gold (Analytical Layer)
- `breweries_aggregated.csv`: Dados agregados por localização e tipo de cervejaria

## Regras de Transformação

### Silver Layer
- Remoção de campos desnecessários
- Padronização de nomes de colunas
- Conversão de tipos de dados

### Gold Layer
- Agregação por localização e tipo de cervejaria
- Cálculo de contagens

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

## Monitoramento e Alertas

O monitoramento é realizado através da interface web do Airflow, que fornece visualizações detalhadas do status de cada tarefa e do DAG como um todo. Para alertas, configuramos notificações por e-mail em caso de falhas nas tarefas críticas do pipeline.

## Tratamento de Erros

O pipeline inclui tratamento de erros para lidar com falhas na API, problemas de conexão e inconsistências nos dados. Logs detalhados são gerados em cada etapa para facilitar a identificação e resolução de problemas.

## Considerações de Segurança

- As credenciais e chaves sensíveis são armazenadas como variáveis de ambiente e não são expostas no código-fonte.
- O acesso à interface web do Airflow é protegido por autenticação.

## Próximos Passos e Melhorias Futuras

- Implementar testes unitários e de integração mais abrangentes
- Otimizar o desempenho do processamento para volumes maiores de dados
- Expandir as capacidades analíticas da camada Gold

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

Para quaisquer dúvidas ou sugestões, por favor, abra uma issue neste repositório ou me ligue.
