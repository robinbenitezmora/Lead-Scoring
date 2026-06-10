"""
Cliente externo de prueba para la API de scoring.

Carga payload.json, realiza llamada HTTP a /predict y muestra la respuesta.
"""

import json
import requests
from pathlib import Path

# Configuración
API_URL = "http://127.0.0.1:8000"
PAYLOAD_FILE = Path(__file__).parent / "payload.json"

print("=" * 80)
print("CLIENTE DE PRUEBA — API DE SCORING")
print("=" * 80)

# 1. Cargar payload
print(f"\n1. Cargando payload desde: {PAYLOAD_FILE}")
if not PAYLOAD_FILE.exists():
    print(f"   ❌ Archivo no encontrado")
    exit(1)

with open(PAYLOAD_FILE, 'r') as f:
    payload = json.load(f)

print(f"   ✅ {len(payload)} registros cargados")

# 2. Realizar llamada HTTP
print(f"\n2. Llamando a {API_URL}/predict...")
try:
    response = requests.post(
        f"{API_URL}/predict",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")
    exit(1)

# 3. Procesar respuesta
print(f"\n3. Respuesta HTTP:")
print(f"   Status Code: {response.status_code}")
print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")

if response.status_code == 200:
    data = response.json()
    print(f"\n4. Predicciones recibidas:")
    print(f"   Total registros procesados: {data.get('total_registros', 0)}")

    print(f"\n   Resultados:")
    for pred in data.get('predicciones', []):
        print(f"     ID: {pred['id']:<8} | Predicción: {pred['prediction']:<2} | Probabilidad: {pred['probability']:.4f}")

    print(f"\n✅ CLIENTE FUNCIONAL — API respondiendo correctamente")
else:
    print(f"   ❌ Error HTTP: {response.text}")
    exit(1)

print("\n" + "=" * 80)
