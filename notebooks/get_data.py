import os
import requests, sys
import pandas as pd
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError
import logging
from botocore.exceptions import ClientError
# Leer de las variables de entorno
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")

API_SERVER=os.getenv("API_SERVER")
ENDPOINT_ENSG00000139618=os.getenv("ENDPOINT_ENSG00000139618")

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Función para obtener los datos de la API
def getApiData(endpoint):
    r = requests.get(API_SERVER + endpoint, headers=HEADERS)
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    decoded = r.json()
    df = pd.json_normalize(decoded)
    return df

# Función para exportar el DataFrame a un archivo CSV
def exportData(df):   
    filename = f"ensembl_ENSG00000139618_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    return filename

# Función para subir el archivo a S3
def upload_to_s3(file_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    try:
        s3.upload_file(file_name, S3_BUCKET_NAME, file_name)
        print(f"Archivo {file_name} subido exitosamente a S3.")
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
    except NoCredentialsError:
        print("Credenciales no disponibles.")

# Ejecución del proceso
#ENSG00000139618 es el ID de Ensembl para el gen BRCA2, 
# un gen humano importante que está asociado con la predisposición genética a varios tipos de cáncer, 
# incluyendo el cáncer de mama y ovario hereditario. 
# BRCA2 codifica una proteína que es crucial para la reparación del ADN.
df = getApiData(ENDPOINT_ENSG00000139618)
file_name = exportData(df)
upload_to_s3(file_name)
