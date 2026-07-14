# jobs/process_logs.py
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, date_format

def main():
    print("⚡ Iniciando Job de PySpark para el procesamiento de Logs...")

    # 1. Inicializar la sesión de Spark optimizada para entorno local
    spark = SparkSession.builder \
        .appName("ECommerce-Logs-Processing") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    # Silenciar logs excesivos de Spark para ver claro nuestro output
    spark.sparkContext.setLogLevel("WARN")

    input_path = "data/web_logs.csv"
    output_path = "output/web_logs_clean"

    # Verificar que el archivo de entrada exista
    if not os.path.exists(input_path):
        print(f"❌ Error: No se encontró el archivo de origen en {input_path}")
        sys.exit(1)

    # 2. Lectura de los datos (Capa Raw / Bronze)
    print(f"📖 Leyendo datos desde {input_path}...")
    raw_logs = spark.read.csv(input_path, header=True, inferSchema=True)
    
    print(f"📊 Cantidad de registros iniciales: {raw_logs.count()}")
    raw_logs.printSchema()

    # 3. Transformaciones y Limpieza (Capa Staging / Silver)
    # - Filtramos registros donde el user_id sea nulo
    # - Parseamos el timestamp para asegurar que Spark lo entienda como fecha/hora real
    # - Creamos una columna 'fecha' (formato YYYY-MM-DD) para usar como partición física
    print("🧹 Aplicando transformaciones y limpieza...")
    clean_logs = raw_logs \
        .filter(col("user_id").isNotNull()) \
        .withColumn("parsed_timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")) \
        .withColumn("fecha", date_format(col("parsed_timestamp"), "yyyy-MM-dd")) \
        .drop("timestamp")  # Eliminamos la columna de texto vieja

    print(f"📊 Cantidad de registros limpios: {clean_logs.count()}")

    # 4. Escritura en formato Parquet particionado (Capa Silver de salida)
    print(f"💾 Guardando datos limpios en formato Parquet en: {output_path}...")
    
    clean_logs.write \
        .mode("overwrite") \
        .partitionBy("fecha") \
        .parquet(output_path)

    print("✅ Job de PySpark finalizado con éxito de forma local.")
    spark.stop()

if __name__ == "__main__":
    main()