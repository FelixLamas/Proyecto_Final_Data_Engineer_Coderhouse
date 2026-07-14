# Proyecto Final Curso Data Engineer Coderhouse

Pipeline de datos end-to-end diseñado bajo una **Arquitectura Medallion** (Raw/Bronze, Staging/Silver, Marts/Gold) para procesar eventos de clickstream e ingresos de ventas.

## 🛠️ Tecnologías Utilizadas
* **Procesamiento Distribuido:** PySpark
* **Data Warehouse Analítico (Local):** DuckDB
* **Ingeniería Analítica:** dbt-core & dbt-duckdb
* **Orquestación:** Apache Airflow
* **Contenedores:** Docker & Docker Compose

## 📂 Estructura del Proyecto
* `data/`: Datos de entrada (Raw) y salidas intermedias (Parquet).
* `jobs/`: Scripts de procesamiento en Python y Spark.
* `models/`: Directorio de modelos SQL de dbt.
* `tests/`: Validaciones y pruebas de calidad de datos.
* `output/`: Ubicación de la base de datos DuckDB persistida.

## 🚀 Guía de Inicio Rápido
*(Próximamente se detallarán los pasos de ejecución de los containers y DAGs)*