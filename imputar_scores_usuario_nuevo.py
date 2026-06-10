import pandas as pd
import json
from datetime import datetime

# Configuración
input_path = r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean_v2.csv'
output_path = r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean_v3.csv'
log_path = r'c:\Users\robin\dev\01_LEADSCORING\06_resultados\imputacion_log.json'

# Columnas a imputar
columnas_scores = ['score_actividad', 'score_perfil']

print("=" * 90)
print("IMPUTACIÓN DE SCORES Y CREACIÓN DE VARIABLE USUARIO_NUEVO")
print("=" * 90)

# Cargar datos
df = pd.read_csv(input_path, sep=';')
print(f"\n📥 Datos cargados: {len(df):,} registros, {len(df.columns)} columnas\n")

# ESTADO ACTUAL
print("ESTADO ACTUAL DE NULOS:")
print("-" * 90)
for col in columnas_scores:
    n_nulos = df[col].isna().sum()
    pct = (n_nulos / len(df)) * 100
    print(f"  {col:<25} Nulos: {n_nulos:>6} ({pct:>6.2f}%)")

# IDENTIFICAR REGISTROS A IMPUTAR
# Crear máscara para registros con nulos en AMBAS columnas
mask_ambos_nulos = df[columnas_scores].isna().all(axis=1)
n_imputar = mask_ambos_nulos.sum()

print(f"\n⚠️  Registros CON nulos en AMBAS columnas (usuario_nuevo = 1): {n_imputar:,}")
print(f"   Porcentaje: {(n_imputar / len(df)) * 100:.2f}%")

# Registros sin imputación
mask_sin_imputacion = ~mask_ambos_nulos
n_sin_imputacion = mask_sin_imputacion.sum()

print(f"\n✓  Registros SIN imputación (usuario_nuevo = 0): {n_sin_imputacion:,}")
print(f"   Porcentaje: {(n_sin_imputacion / len(df)) * 100:.2f}%")

# MOSTRAR EJEMPLOS DE REGISTROS A IMPUTAR
if n_imputar > 0:
    print(f"\n📌 EJEMPLOS DE REGISTROS A IMPUTAR (primeros 10):")
    print("-" * 90)
    cols_display = ['id', 'origen', 'score_actividad', 'score_perfil', 'tiene_score_actividad', 'tiene_score_perfil']
    df_imputar = df[mask_ambos_nulos][cols_display].head(10)
    print(df_imputar.to_string())

# CREAR VARIABLE USUARIO_NUEVO ANTES DE IMPUTAR
df['usuario_nuevo'] = 0
df.loc[mask_ambos_nulos, 'usuario_nuevo'] = 1

print(f"\n\n✅ VARIABLE USUARIO_NUEVO CREADA:")
print("-" * 90)
print(df['usuario_nuevo'].value_counts().sort_index().to_string())

# IMPUTAR NULOS CON CEROS
print(f"\n\n🔄 IMPUTACIÓN DE NULOS CON CEROS:")
print("-" * 90)

for col in columnas_scores:
    n_nulos_antes = df[col].isna().sum()
    df[col] = df[col].fillna(0)
    n_nulos_despues = df[col].isna().sum()

    print(f"  {col:<25} {n_nulos_antes:>6} → {n_nulos_despues:>6}")

# VALIDACIÓN POST-IMPUTACIÓN
print(f"\n\n🔍 VALIDACIÓN POST-IMPUTACIÓN:")
print("-" * 90)
for col in columnas_scores:
    n_nulos = df[col].isna().sum()
    if n_nulos == 0:
        print(f"  ✓ {col:<25} Sin nulos")
    else:
        print(f"  ✗ {col:<25} ¡Aún tiene {n_nulos} nulos!")

# ESTADÍSTICAS DE USUARIO_NUEVO
print(f"\n\n📊 ESTADÍSTICAS DE USUARIO_NUEVO:")
print("-" * 90)

for val in [0, 1]:
    subset = df[df['usuario_nuevo'] == val]
    n = len(subset)
    pct = (n / len(df)) * 100

    label = "No imputado" if val == 0 else "Imputado (nuevo)"
    print(f"\n  usuario_nuevo = {val} ({label}): {n:,} ({pct:.2f}%)")

    # Estadísticas de scores en este grupo
    for col in columnas_scores:
        mean_val = subset[col].mean()
        print(f"    {col:<24} Media: {mean_val:>8.2f}")

# CORRELACIÓN CON TARGET
print(f"\n\n🎯 CORRELACIÓN CON VARIABLE TARGET (compra):")
print("-" * 90)

for col in ['usuario_nuevo'] + columnas_scores:
    if df[col].dtype in ['int64', 'float64']:
        mask = df[col].notna() & df['compra'].notna()
        if mask.sum() > 0:
            corr = df.loc[mask, col].corr(df.loc[mask, 'compra'])
            print(f"  {col:<25} Correlación: {corr:>8.4f}")

# GUARDAR ARCHIVO
df.to_csv(output_path, sep=';', index=False)
print(f"\n\n📤 Archivo guardado en: {output_path}")

# CREAR REPORTE DE LOG
reporte = {
    'fecha_imputacion': datetime.now().isoformat(),
    'archivo_original': input_path,
    'archivo_nuevo': output_path,
    'columnas_imputadas': columnas_scores,
    'nueva_variable': 'usuario_nuevo',
    'estadisticas': {
        'registros_totales': int(len(df)),
        'registros_imputados': int(n_imputar),
        'registros_sin_imputar': int(n_sin_imputacion),
        'pct_imputados': round((n_imputar / len(df)) * 100, 2),
        'pct_sin_imputar': round((n_sin_imputacion / len(df)) * 100, 2)
    },
    'detalles_por_columna': {}
}

for col in columnas_scores:
    media_total = df[col].mean()
    media_imputados = df[df['usuario_nuevo'] == 1][col].mean()
    media_no_imputados = df[df['usuario_nuevo'] == 0][col].mean()

    reporte['detalles_por_columna'][col] = {
        'media_total': round(float(media_total), 4),
        'media_usuarios_nuevos': round(float(media_imputados), 4),
        'media_usuarios_existentes': round(float(media_no_imputados), 4),
        'zeros_imputados': int((df[df['usuario_nuevo'] == 1][col] == 0).sum())
    }

# Agregar estadísticas de usuario_nuevo
usuario_nuevo_stats = df['usuario_nuevo'].value_counts().sort_index()
reporte['usuario_nuevo_distribution'] = {
    str(int(k)): int(v) for k, v in usuario_nuevo_stats.items()
}

# Guardar reporte
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(reporte, f, indent=2, ensure_ascii=False)

print(f"📊 Reporte guardado en: {log_path}")

print(f"\n\n" + "=" * 90)
print("✨ IMPUTACIÓN Y CREACIÓN DE VARIABLE COMPLETADA")
print("=" * 90)
print(f"\n📋 RESUMEN FINAL:")
print(f"   • Registros totales: {len(df):,}")
print(f"   • Usuarios nuevos (imputados): {n_imputar:,} ({(n_imputar / len(df) * 100):.2f}%)")
print(f"   • Usuarios existentes: {n_sin_imputacion:,} ({(n_sin_imputacion / len(df) * 100):.2f}%)")
print(f"   • Columnas imputadas: {', '.join(columnas_scores)}")
print(f"   • Variable nueva creada: usuario_nuevo")
print(f"\n✅ Datos listos para siguiente fase\n")
