import os
import pandas as pd
import boto3
import psycopg2
import psycopg2.extras as extras
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Cargar variables de entorno
load_dotenv()

# Leer las credenciales de AWS y RDS desde el archivo .env
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
RDS_HOSTNAME = os.getenv("RDS_HOSTNAME")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_DBNAME = os.getenv("RDS_DBNAME")
RDS_PORT = os.getenv("RDS_PORT")

# Conexión a S3
s3_client = boto3.client(
    's3', 
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

# Descargar archivo de S3
def download_file_from_s3(bucket, s3_file_name, local_file_path):
    try:
        s3_client.download_file(bucket, s3_file_name, local_file_path)
    except ClientError:
        return False
    return True

bucket_name = S3_BUCKET_NAME
s3_file_name = 'input-data/ensembl_ENSG00000139618_20241017_200540.csv'
#local_file_path = 'ensembl_ENSG00000139618_download.csv'
local_file_path = '/tmp/ensembl_data.csv'

download_file_from_s3(bucket_name, s3_file_name, local_file_path)

# Preprocesar datos
data = pd.read_csv(local_file_path)

# Manejo de valores vacíos en 'clinical_significance'
data['clinical_significance'] = data['clinical_significance'].apply(
    lambda x: 'other' if x == '[]' or pd.isna(x) else x)

# Convertir 'alleles' a texto plano
data['alleles'] = data['alleles'].str.strip("[]").str.replace("'", "").str.replace(" ", "")

# Eliminar columnas innecesarias
columns_to_drop = ['source', 'assembly_name', 'seq_region_name', 'id']
data_filtered = data.drop(columns=columns_to_drop)

# Agrupación de 'clinical_significance'
def group_clinical_significance(value):
    if 'benign' in value:
        return 'benign'
    elif 'pathogenic' in value:
        return 'pathogenic'
    elif 'uncertain significance' in value:
        return 'uncertain_significance'
    else:
        return 'other'

data_filtered['clinical_significance'] = data_filtered['clinical_significance'].apply(group_clinical_significance)

# Renombrar columna 'end' a 'end_position' si existe
if 'end' in data_filtered.columns:
    data_filtered = data_filtered.rename(columns={'end': 'end_position'})

# Asegurarse de que las columnas numéricas tengan valores válidos
data_filtered['strand'] = pd.to_numeric(data_filtered['strand'], errors='coerce')
data_filtered['start'] = pd.to_numeric(data_filtered['start'], errors='coerce')
data_filtered['end_position'] = pd.to_numeric(data_filtered['end_position'], errors='coerce')

# Eliminar filas con NaN en columnas clave
data_filtered = data_filtered.dropna(subset=['strand', 'start', 'end_position'])

# Limitar el DataFrame a 5000 registros
data_filtered = data_filtered.head(30000)

# Función para guardar datos en RDS en lotes
def save_to_rds_batch(dataframe, batch_size=100):
    try:
        conn = psycopg2.connect(
            host=RDS_HOSTNAME,
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            dbname=RDS_DBNAME,
            port=RDS_PORT
        )
        cursor = conn.cursor()

        # Convertir DataFrame a lista de tuplas
        tuples = [tuple(x) for x in dataframe.to_numpy()]

        # Query de inserción
        query = """
        INSERT INTO preprocessed_data 
        (consequence_type, clinical_significance, feature_type, start, end_position, strand, alleles) 
        VALUES %s
        """
        
        # Insertar los datos en lotes
        for i in range(0, len(tuples), batch_size):
            batch = tuples[i:i+batch_size]
            extras.execute_values(cursor, query, batch)
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        pass

# Guardar los datos preprocesados en lotes
save_to_rds_batch(data_filtered, batch_size=100)
