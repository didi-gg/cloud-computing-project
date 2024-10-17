# Data Processing Service

Este directorio contiene la configuración y scripts para el **preprocesamiento de datos** genómicos antes de que estos se utilicen en el entrenamiento de modelos de machine learning.

## **Descripción**

El servicio de **preprocesamiento de datos** se ejecuta en un contenedor de Docker y realiza tareas como la carga, limpieza y transformación de los datos genómicos. Los resultados son almacenados en una base de datos para el siguiente paso en el flujo de trabajo de machine learning.

### **Estructura del Contenido**

- **`Dockerfile`**: Define cómo se construye el contenedor para preprocesar los datos. Utiliza una imagen base de **Python 3.9** e instala las dependencias necesarias para procesar datos.