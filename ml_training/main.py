import os
import pandas as pd
import boto3
import psycopg2
from psycopg2 import extras
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Leer las credenciales desde las variables de entorno
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

# Cargar datos preprocesados desde RDS
def load_from_rds():
    try:
        conn = psycopg2.connect(
            host=RDS_HOSTNAME,
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            dbname=RDS_DBNAME,
            port=RDS_PORT
        )
        query = "SELECT * FROM preprocessed_data"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error al cargar los datos desde RDS: {e}")
        return None

# Cargar los datos preprocesados desde RDS
data_filtered = load_from_rds()

if data_filtered is None:
    print("Error al cargar los datos, deteniendo el proceso.")
    exit()

# Codificar las columnas categóricas
le = LabelEncoder()

# Codificar 'clinical_significance' y otras columnas categóricas
data_filtered['clinical_significance'] = le.fit_transform(data_filtered['clinical_significance'])

categorical_columns = ['consequence_type', 'alleles', 'feature_type']
for col in categorical_columns:
    data_filtered[col] = le.fit_transform(data_filtered[col])

# Separar las variables independientes (X) y la dependiente (y)
X = data_filtered.drop(columns=['clinical_significance'])
y = data_filtered['clinical_significance']

# Dividir los datos en entrenamiento y prueba (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predecir en el conjunto de prueba
y_pred = rf_model.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Exactitud del modelo: {accuracy:.4f}")
print("Reporte de Clasificación:")
print(classification_report(y_test, y_pred))

# Guardar los resultados de predicción en RDS
def save_predictions_to_rds(X_test, predictions):
    try:
        conn = psycopg2.connect(
            host=RDS_HOSTNAME,
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            dbname=RDS_DBNAME,
            port=RDS_PORT
        )
        cursor = conn.cursor()
        for idx, pred in enumerate(predictions):
            cursor.execute("INSERT INTO predictions (variation_id, prediction) VALUES (%s, %s)",
                           (X_test.index[idx].item(), pred.item()))
        conn.commit()
        cursor.close()
        conn.close()
        print("Predicciones guardadas exitosamente en RDS.")
    except Exception as e:
        print(f"Error al guardar las predicciones en RDS: {e}")

# Guardar las predicciones en RDS
save_predictions_to_rds(X_test, y_pred)
