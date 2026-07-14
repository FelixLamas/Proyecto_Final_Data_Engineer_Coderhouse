{{ config(materialized='table') }}

WITH usuarios AS (
    SELECT * FROM {{ ref('stg_usuarios') }}
),

ventas AS (
    SELECT 
        user_id,
        SUM(cantidad * precio_unitario) AS total_gastado,
        COUNT(DISTINCT transaction_id) AS total_transacciones
    FROM {{ ref('stg_ventas') }}
    GROUP BY 1
),

logs_agrupados AS (
    SELECT
        user_id,
        COUNT(CASE WHEN action = 'view' THEN 1 END) AS total_vistas,
        COUNT(CASE WHEN action = 'add_to_cart' THEN 1 END) AS total_agregados_carrito,
        COUNT(CASE WHEN action = 'purchase' THEN 1 END) AS total_compras_clickstream
    FROM {{ ref('stg_web_logs') }}
    GROUP BY 1
)

SELECT
    u.user_id,
    u.nombre,
    u.pais,
    u.fecha_registro,
    COALESCE(la.total_vistas, 0) AS total_vistas,
    COALESCE(la.total_agregados_carrito, 0) AS total_agregados_carrito,
    COALESCE(la.total_compras_clickstream, 0) AS total_compras_clickstream,
    COALESCE(v.total_transacciones, 0) AS compras_reales_facturacion,
    COALESCE(v.total_gastado, 0.0) AS ingresos_totales_usuario
FROM usuarios u
LEFT JOIN logs_agrupados la ON u.user_id = la.user_id
LEFT JOIN ventas v ON u.user_id = v.user_id