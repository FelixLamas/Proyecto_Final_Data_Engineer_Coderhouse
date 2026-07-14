{{ config(materialized='view') }}

SELECT
    CAST(transaction_id AS VARCHAR) AS transaction_id,
    CAST(user_id AS VARCHAR) AS user_id,
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(cantidad AS INTEGER) AS cantidad,
    CAST(precio_unitario AS DOUBLE) AS precio_unitario,
    CAST(fecha AS DATE) AS fecha
FROM read_parquet('data/ventas.parquet')