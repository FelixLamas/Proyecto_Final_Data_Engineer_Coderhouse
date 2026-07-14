{{ config(materialized='view') }}

-- DuckDB lee de manera ultra rápida toda la estructura de carpetas Parquet particionadas por PySpark
SELECT
    CAST(user_id AS VARCHAR) AS user_id,
    CAST(page_url AS VARCHAR) AS page_url,
    CAST(action AS VARCHAR) AS action,
    CAST(parsed_timestamp AS TIMESTAMP) AS timestamp,
    CAST(fecha AS DATE) AS fecha
FROM read_parquet('output/web_logs_clean/**/*.parquet')