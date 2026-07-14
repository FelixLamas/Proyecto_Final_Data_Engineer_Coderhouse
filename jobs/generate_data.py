import os
import random
from datetime import datetime, timedelta
import pandas as pd


os.makedirs("data", exist_ok=True)

print("⏳ Iniciando la generación de datos sintéticos...")

# Configuración básica
num_usuarios = 100
num_ventas = 300
num_logs = 1000
fecha_inicio = datetime(2026, 6, 1)

# 1. GENERAR USUARIOS (usuarios.csv)
paises = ["Argentina", "Brasil", "Chile", "Uruguay", "Colombia"]
usuarios_data = {
    "user_id": [f"USR_{i:04d}" for i in range(1, num_usuarios + 1)],
    "nombre": [f"Usuario_{i}" for i in range(1, num_usuarios + 1)],
    "pais": [random.choice(paises) for _ in range(num_usuarios)],
    "fecha_registro": [
        (fecha_inicio - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        for _ in range(num_usuarios)
    ],
}
df_usuarios = pd.DataFrame(usuarios_data)
df_usuarios.to_csv("data/usuarios.csv", index=False)
print("✅ Archivo 'data/usuarios.csv' generado con éxito.")

# 2. GENERAR VENTAS (ventas.parquet)
productos = [
    {"id": "PROD_01", "precio": 1500.0},
    {"id": "PROD_02", "precio": 2500.5},
    {"id": "PROD_03", "precio": 4300.0},
    {"id": "PROD_04", "precio": 990.99},
    {"id": "PROD_05", "precio": 7500.0},
]

ventas_data = []
for i in range(1, num_ventas + 1):
    prod = random.choice(productos)
    fecha_venta = fecha_inicio + timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    ventas_data.append(
        {
            "transaction_id": f"TX_{i:05d}",
            "user_id": random.choice(df_usuarios["user_id"]),
            "product_id": prod["id"],
            "cantidad": random.randint(1, 5),
            "precio_unitario": prod["precio"],
            "fecha": fecha_venta.strftime("%Y-%m-%d"),
        }
    )

df_ventas = pd.DataFrame(ventas_data)
df_ventas.to_parquet("data/ventas.parquet", index=False)
print("✅ Archivo 'data/ventas.parquet' generado con éxito.")

# 3. GENERAR LOGS WEB (web_logs.csv)
acciones = ["view", "add_to_cart", "purchase"]
urls_productos = [f"/product/{prod['id']}" for prod in productos]
urls_generales = ["/home", "/search", "/cart", "/checkout"]

logs_data = []
for _ in range(num_logs):
    user_id = random.choice(df_usuarios["user_id"])
    action = random.choice(acciones)

    # Lógica para que la URL tenga sentido según la acción
    if action in ["add_to_cart", "purchase"]:
        page_url = random.choice(urls_productos)
    else:
        page_url = random.choice(urls_generales + urls_productos)

    timestamp = fecha_inicio + timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )

    logs_data.append(
        {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "page_url": page_url,
            "action": action,
        }
    )

df_logs = pd.DataFrame(logs_data)
df_logs.to_csv("data/web_logs.csv", index=False)
print("✅ Archivo 'data/web_logs.csv' generado con éxito.")
print("🚀 ¡Todos los datasets de prueba están listos en la carpeta data/!")