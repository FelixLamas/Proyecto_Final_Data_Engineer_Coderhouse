# run_pipeline.py
import subprocess
import sys
import time
from prometheus_client import start_http_server, Gauge, Counter

# 1. Definición de Métricas para Prometheus
# Un Gauge (indicador) para saber el estado general del último pipeline run (1 = Éxito, 0 = Fallo)
PIPELINE_STATUS = Gauge(
    'data_pipeline_status', 
    'Estado de la ultima ejecucion del pipeline (1=Exito, 0=Fallo)'
)

# Un Gauge que rastrea cuánto tiempo tardó cada tarea individual usando etiquetas (labels)
TASK_DURATION = Gauge(
    'data_pipeline_task_duration_seconds', 
    'Tiempo de ejecucion de cada tarea en segundos', 
    ['task_name']
)

# Un Counter (contador acumulativo) para registrar la cantidad total de ejecuciones
PIPELINE_RUNS_TOTAL = Counter(
    'data_pipeline_runs_total', 
    'Cantidad total de veces que se ejecuto el pipeline completo',
    ['status']
)

def run_command(command, description, task_metric_name):
    """Ejecuta un comando de sistema, mide su tiempo y actualiza las métricas."""
    print("\n" + "="*60)
    print(f"🚀 [TASK START]: {description}")
    print(f"💻 Comando: {command}")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    # Ejecución del subproceso en tiempo real
    process = subprocess.Popen(command, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    process.communicate()
    
    elapsed_time = time.time() - start_time
    
    if process.returncode != 0:
        print("\n" + "!"*60)
        print(f"❌ [TASK FAILED]: {description} falló con código {process.returncode}.")
        print("!"*60 + "\n")
        
        # En caso de fallo, reportamos estado 0 a Prometheus y salimos
        PIPELINE_STATUS.set(0)
        PIPELINE_RUNS_TOTAL.labels(status='failed').inc()
        time.sleep(2)  # Pequeña pausa para asegurar que Prometheus alcance a leer el fallo
        sys.exit(process.returncode)
    
    # Si la tarea fue exitosa, registramos su duración en Prometheus
    TASK_DURATION.labels(task_name=task_metric_name).set(elapsed_time)
    
    print("\n" + "="*60)
    print(f"✅ [TASK SUCCESS]: {description} completado en {elapsed_time:.2f} segundos.")
    print("="*60 + "\n")

def main():
    # 2. Iniciar el servidor de métricas de Prometheus en el puerto 8000
    # Este puerto es el que scrapeará el contenedor de Prometheus
    print("📡 Iniciando servidor de métricas de Prometheus en http://localhost:8000/metrics...")
    start_http_server(8000)

    print("🏁 INICIANDO PIPELINE DE DATOS ANALÍTICOS (Monitoreado)")
    pipeline_start = time.time()

    try:
        # Task 1: Ingesta / Generación de Datos
        run_command(
            "python jobs/generate_data.py", 
            "Generación de Datos Sintéticos",
            "generate_data"
        )
        
        # Task 2: PySpark
        run_command(
            "python jobs/process_logs.py", 
            "Procesamiento Clickstream con PySpark",
            "pyspark_logs"
        )
        
        # Task 3: dbt Run
        run_command(
            "dbt run", 
            "Compilación y Carga de Modelos en dbt",
            "dbt_run"
        )
        
        # Task 4: dbt Test
        run_command(
            "dbt test", 
            "Validación de Calidad de Datos (dbt tests)",
            "dbt_test"
        )
        
        total_time = time.time() - pipeline_start
        print(f"🎉 ¡PIPELINE FINALIZADO CON ÉXITO en {total_time:.2f} segundos! 🎉")
        
        PIPELINE_STATUS.set(1)
        PIPELINE_RUNS_TOTAL.labels(status='success').inc()
        
        # Aumentamos el tiempo de espera a 60 segundos
        print("⏳ Manteniendo el orquestador activo 60 segundos para que Prometheus recolecte TODAS las métricas...")
        time.sleep(60)
        print("🔌 Apagando servidor de métricas. Proceso finalizado.")

    except Exception as e:
        print(f"💥 Error crítico durante la ejecución del pipeline: {e}")
        PIPELINE_STATUS.set(0)
        PIPELINE_RUNS_TOTAL.labels(status='error').inc()
        time.sleep(5)
        sys.exit(1)

if __name__ == "__main__":
    main()