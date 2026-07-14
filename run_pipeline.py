# run_pipeline.py
import subprocess
import sys
import time

def run_command(command, description):
    """Ejecuta un comando de sistema y maneja los errores como lo haría Airflow."""
    print("\n" + "="*60)
    print(f"🚀 [TASK START]: {description}")
    print(f"💻 Comando: {command}")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    # Ejecutamos el comando y transmitimos la salida en tiempo real
    process = subprocess.Popen(command, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    process.communicate()
    
    elapsed_time = time.time() - start_time
    
    if process.returncode != 0:
        print("\n" + "!"*60)
        print(f"❌ [TASK FAILED]: {description} falló con código {process.returncode}.")
        print("!"*60 + "\n")
        sys.exit(process.returncode)
    
    print("\n" + "="*60)
    print(f"✅ [TASK SUCCESS]: {description} completado en {elapsed_time:.2f} segundos.")
    print("="*60 + "\n")

def main():
    print("🏁 INICIANDO PIPELINE DE DATOS ANALÍTICOS (Simulación de Airflow)")
    pipeline_start = time.time()

    try:
        # Task 1: Generar datos sintéticos (Bronze/Raw Layer)
        run_command(
            "python jobs/generate_data.py", 
            "Generación de Datos Sintéticos"
        )
        
        # Task 2: Procesamiento y particionamiento de logs con PySpark (Silver Layer)
        run_command(
            "python jobs/process_logs.py", 
            "Procesamiento Clickstream con PySpark"
        )
        
        # Task 3: Ejecución de modelos analíticos en dbt (Silver/Gold Layers en DuckDB)
        run_command(
            "dbt run", 
            "Compilación y Carga de Modelos en dbt"
        )
        
        # Task 4: Ejecución de pruebas de calidad e integridad de datos
        run_command(
            "dbt test", 
            "Validación de Calidad de Datos (dbt tests)"
        )
        
        total_time = time.time() - pipeline_start
        print(f"🎉 ¡PIPELINE FINALIZADO CON ÉXITO en {total_time:.2f} segundos! 🎉")

    except Exception as e:
        print(f"💥 Error crítico durante la ejecución del pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()