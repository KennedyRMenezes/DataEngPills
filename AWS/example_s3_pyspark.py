import boto3
import requests
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Configuração do boto3
s3_client = boto3.client('s3')
source_bucket = 'your-source-bucket'  # Bucket de origem
destination_bucket = 'your-destination-bucket'  # Bucket de destino
api_url = 'https://api.example.com/data'  # URL da API

# Função para puxar dados da API
def get_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")

# Configurar o SparkSession
spark = SparkSession.builder \
    .appName("S3 API Data Processing") \
    .config("spark.hadoop.fs.s3a.access.key", "your-access-key") \
    .config("spark.hadoop.fs.s3a.secret.key", "your-secret-key") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .getOrCreate()

# Puxando dados da API
data = get_data_from_api(api_url)

# Transformar dados em DataFrame do Spark
df = spark.read.json(spark.sparkContext.parallelize([json.dumps(data)]))

# Tratar dados (exemplo simples de transformação)
df_transformed = df.select(
    col("id"),
    col("name"),
    col("date").cast("timestamp"),
    col("value").cast("double")
)

# Caminho para salvar os dados no bucket de destino S3
output_path = f"s3a://{destination_bucket}/processed_data.parquet"

# Salvar como Parquet
df_transformed.write.parquet(output_path)

print(f"Dados processados e salvos em: {output_path}")

# Fechar o SparkSession
spark.stop()
