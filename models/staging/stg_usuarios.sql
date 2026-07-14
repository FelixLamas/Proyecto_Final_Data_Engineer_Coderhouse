{{ config(materialized='view') }}

SELECT
    CAST(user_id AS VARCHAR) AS user_id,
    CAST(nombre AS VARCHAR) AS nombre,
    CAST(pais AS VARCHAR) AS pais,
    CAST(fecha_registro AS DATE) AS fecha_registro
FROM read_csv_auto('data/usuarios.csv')