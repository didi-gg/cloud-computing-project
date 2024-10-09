# Cloud Computing Project - Grupo 2. Caso de Uso: Biotech Explorer Corp.

Andrés Felipe Restrepo Melo  
Angie Catherine Ovalle Molina  
Diana Marcela Gómez Gamez  
Liliana del Rosario Arciniegas Mayag  

## Descripción

Esta startup trabaja con análisis de datos genómicos a gran escala. Requiere una infraestructura potente para procesar secuencias genómicas y extraer patrones relevantes para la investigación biotecnológica.

**Solución Propuesta:**
El equipo desarrollará una solución de análisis de datos que use **EC2** para el procesamiento intensivo y una combinación de **RDS** y **S3** para almacenar grandes volúmenes de datos genómicos. Los algoritmos de análisis estarán contenerizados en **Docker** y se desarrollarán en **Python**. Se sugiere el uso de **AWS Batch** para gestionar cargas de trabajo por lotes en la secuenciación genómica, y **EFS** para el almacenamiento compartido.

**Ingresos Operacionales:** US$ 5 millones
**Margen Operacional:** 10%
**Número de Empleados:** 100
**Palabras clave:** Grandes volúmenes, genoma, biotecnología.

## Entregables
### Entregable 1: 
Informe detallado de la arquitectura propuesta, incluyendo diagramas de arquitectura, tipos de instancias EC2, elección de bases de datos RDS, uso de servicios adicionales de AWS, costos estimados y pasos detallados para el despliegue. Cada equipo debe justificar sus decisiones en función de los datos proporcionados y simular los modelos de machine learning o procesos de optimización. 

### Entregable 2: 
Demo en AWS Academy mostrando una versión simplificada de la arquitectura propuesta. El demo debe estar documentado con capturas de pantalla, notebooks de Python, scripts, y un enlace al repositorio de GitHub con el código utilizado. Se deben incluir las URL de acceso a los recursos desplegados, credenciales y endpoints para su revisión. 

### Notas: 
Los modelos o algoritmos no deben ser completamente funcionales. En su lugar, pueden simularse los resultados de predicción con funciones en Python. La arquitectura del demo debe ser coherente pero simplificada para facilitar su despliegue en AWS Academy.
