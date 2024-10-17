# Machine Learning Training Service

Este directorio contiene los archivos necesarios para el **entrenamiento de modelos de machine learning** utilizando los datos preprocesados. El servicio está diseñado para entrenar un modelo y evaluar su rendimiento.

## **Descripción**

El servicio de **entrenamiento de modelos** se ejecuta en un contenedor de Docker, donde se utilizan bibliotecas de machine learning para entrenar un modelo sobre los datos genómicos preprocesados. Los resultados del entrenamiento (como el modelo entrenado o las métricas de rendimiento) se guardan en una base de datos.

### **Estructura del Contenido**

- **`Dockerfile`**: Define la construcción del contenedor de machine learning. Instala las dependencias necesarias como **scikit-learn**, **pandas**, y **numpy**.