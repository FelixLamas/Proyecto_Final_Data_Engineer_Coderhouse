-- tests/assert_precio_es_positivo.sql
-- Este test busca registros que rompan la regla. Si la consulta devuelve filas, el test FALLA.
SELECT
    transaction_id,
    precio_unitario
FROM {{ ref('stg_ventas') }}
WHERE precio_unitario <= 0