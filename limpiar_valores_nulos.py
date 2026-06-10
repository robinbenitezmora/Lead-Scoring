import pandas as pd
import json
from datetime import datetime

# Configuración
input_path = r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean.csv'
output_path = r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean_v2.csv'
log_path = r'c:\Users\robin\dev\01_LEADSCORING\06_resultados\limpieza_log.json'

# Columnas que no deben tener nulos
columnas_criticas = ['visitas_total', 'paginas_vistas_visita']

print("=" * 80)
print("LIMPIEZA DE REGISTROS CON VALORES NULOS")
print("=" * 80)

# Cargar datos
df = pd.read_csv(input_path, sep=';')
print(f"\n📥 Datos cargados: {len(df):,} registros, {len(df.columns)} columnas\n")

# Mostrar estado actual
print("ESTADO ACTUAL:")
print("-" * 80)
for col in columnas_criticas:
    n_nulos = df[col].isna().sum()
    pct = (n_nulos / len(df)) * 100
    print(f"  {col:<25} Nulos: {n_nulos:>6} ({pct:>6.2f}%)")

# Identificar registros con nulos en cualquiera de estas columnas
mask_nulos = df[columnas_criticas].isna().any(axis=1)
n_registros_nulos = mask_nulos.sum()

print(f"\n⚠️  Registros con nulos EN CUALQUIERA de estas columnas: {n_registros_nulos:,}")
print(f"   Porcentaje: {(n_registros_nulos / len(df)) * 100:.2f}%")

# Mostrar detalles de registros a eliminar
print(f"\n📋 DETALLES DE REGISTROS A ELIMINAR:")
print("-" * 80)

df_con_nulos = df[mask_nulos]
for col in columnas_criticas:
    n = df_con_nulos[col].isna().sum()
    print(f"  {col:<25} {n:>6} registros con nulos")

print(f"\n  Total único de registros a eliminar: {n_registros_nulos:,}")

# Mostrar algunos ejemplos de registros a eliminar
print(f"\n📌 EJEMPLOS DE REGISTROS A ELIMINAR (primeros 5):")
print("-" * 80)
cols_display = ['id', 'origen', 'visitas_total', 'paginas_vistas_visita', 'compra']
print(df_con_nulos[cols_display].head().to_string())

# Eliminar registros
df_limpio = df[~mask_nulos].copy()
n_eliminados = len(df) - len(df_limpio)

print(f"\n\n✅ LIMPIEZA REALIZADA:")
print("-" * 80)
print(f"  Registros originales:      {len(df):,}")
print(f"  Registros eliminados:      {n_eliminados:,}")
print(f"  Registros finales:         {len(df_limpio):,}")
print(f"  Tasa de retención:         {(len(df_limpio) / len(df)) * 100:.2f}%")

# Validar que no quedan nulos en estas columnas
print(f"\n\n🔍 VALIDACIÓN POST-LIMPIEZA:")
print("-" * 80)
for col in columnas_criticas:
    n_nulos = df_limpio[col].isna().sum()
    if n_nulos == 0:
        print(f"  ✓ {col:<25} Sin nulos")
    else:
        print(f"  ✗ {col:<25} ¡Aún tiene {n_nulos} nulos!")

# Guardar archivo limpio
df_limpio.to_csv(output_path, sep=';', index=False)
print(f"\n\n📤 Archivo guardado en: {output_path}")

# Crear reporte de log
reporte = {
    'fecha_limpieza': datetime.now().isoformat(),
    'archivo_original': input_path,
    'archivo_limpio': output_path,
    'columnas_criticas': columnas_criticas,
    'estadisticas': {
        'registros_originales': int(len(df)),
        'registros_eliminados': int(n_eliminados),
        'registros_finales': int(len(df_limpio)),
        'tasa_retencion_pct': round((len(df_limpio) / len(df)) * 100, 2),
        'tasa_eliminacion_pct': round((n_eliminados / len(df)) * 100, 2)
    },
    'detalles_por_columna': {}
}

for col in columnas_criticas:
    nulos_original = int(df[col].isna().sum())
    nulos_final = int(df_limpio[col].isna().sum())
    reporte['detalles_por_columna'][col] = {
        'nulos_original': nulos_original,
        'nulos_final': nulos_final,
        'pct_nulos_original': round((nulos_original / len(df)) * 100, 2)
    }

# Guardar reporte
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(reporte, f, indent=2, ensure_ascii=False)

print(f"📊 Reporte guardado en: {log_path}")

print("\n" + "=" * 80)
print("✨ LIMPIEZA COMPLETADA")
print("=" * 80)
