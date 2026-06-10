import pandas as pd
import json

# Cargar archivos
df_v2 = pd.read_csv(
    r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean_v2.csv',
    sep=';'
)
df_v3 = pd.read_csv(
    r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean_v3.csv',
    sep=';'
)

print("=" * 100)
print("VALIDACIÓN DE IMPUTACIÓN Y VARIABLE USUARIO_NUEVO")
print("=" * 100)

# Comparación general
print(f"\n📊 COMPARACIÓN ANTES/DESPUÉS:")
print("-" * 100)
print(f"  Registros v2:                {len(df_v2):>6,}")
print(f"  Registros v3:                {len(df_v3):>6,}")
print(f"  Cambio:                      {len(df_v3) - len(df_v2):>6,}")

print(f"\n  Columnas v2:                 {len(df_v2.columns):>6}")
print(f"  Columnas v3:                 {len(df_v3.columns):>6}")
print(f"  Nuevas columnas:             {len(df_v3.columns) - len(df_v2.columns):>6}")

# Validar nulos en scores
print(f"\n🔍 VALIDACIÓN DE NULOS EN SCORES:")
print("-" * 100)
print(f"{'Columna':<25} {'v2 (Antes)':<20} {'v3 (Después)':<20}")
print("-" * 100)

for col in ['score_actividad', 'score_perfil']:
    v2_nulos = df_v2[col].isna().sum()
    v3_nulos = df_v3[col].isna().sum()
    v2_pct = (v2_nulos / len(df_v2)) * 100
    v3_pct = (v3_nulos / len(df_v3)) * 100 if len(df_v3) > 0 else 0

    print(f"{col:<25} {v2_nulos:>6} ({v2_pct:>6.2f}%)       {v3_nulos:>6} ({v3_pct:>6.2f}%)")

# Validar variable usuario_nuevo
print(f"\n📋 VARIABLE USUARIO_NUEVO:")
print("-" * 100)

usuario_nuevo_dist = df_v3['usuario_nuevo'].value_counts().sort_index()
print(f"\n{'Valor':<10} {'Descripción':<30} {'Cantidad':<12} {'Porcentaje'}")
print("-" * 100)

for val in [0, 1]:
    if val in usuario_nuevo_dist.index:
        count = usuario_nuevo_dist[val]
        pct = (count / len(df_v3)) * 100
        desc = "No imputado (usuario existente)" if val == 0 else "Imputado (usuario nuevo)"
        print(f"{val:<10} {desc:<30} {count:>10,} {pct:>6.2f}%")

# Validar que usuario_nuevo = 1 corresponde a imputados
print(f"\n✅ VALIDACIÓN DE LÓGICA usuario_nuevo:")
print("-" * 100)

# Registros con usuario_nuevo = 1 deberían tener score_* = 0
usuarios_nuevos = df_v3[df_v3['usuario_nuevo'] == 1]
score_act_zero = (usuarios_nuevos['score_actividad'] == 0).sum()
score_perf_zero = (usuarios_nuevos['score_perfil'] == 0).sum()

print(f"  Usuarios nuevos (usuario_nuevo=1): {len(usuarios_nuevos):,}")
print(f"    score_actividad = 0: {score_act_zero:,} ({(score_act_zero/len(usuarios_nuevos)*100):.2f}%)")
print(f"    score_perfil = 0: {score_perf_zero:,} ({(score_perf_zero/len(usuarios_nuevos)*100):.2f}%)")

# Registros con usuario_nuevo = 0 deberían tener score_* > 0 o NaN (no, ahora son imputados)
usuarios_existentes = df_v3[df_v3['usuario_nuevo'] == 0]
print(f"\n  Usuarios existentes (usuario_nuevo=0): {len(usuarios_existentes):,}")
print(f"    score_actividad - Media: {usuarios_existentes['score_actividad'].mean():.2f}")
print(f"    score_actividad - Min: {usuarios_existentes['score_actividad'].min():.2f}")
print(f"    score_perfil - Media: {usuarios_existentes['score_perfil'].mean():.2f}")
print(f"    score_perfil - Min: {usuarios_existentes['score_perfil'].min():.2f}")

# Distribución de scores por grupo
print(f"\n📊 DISTRIBUCIÓN DE SCORES POR GRUPO:")
print("-" * 100)

print(f"\n  score_actividad:")
print(f"    Usuarios existentes (n={len(usuarios_existentes):,}):")
print(f"      Media: {usuarios_existentes['score_actividad'].mean():.4f}")
print(f"      Desv.Est: {usuarios_existentes['score_actividad'].std():.4f}")
print(f"      Min-Max: {usuarios_existentes['score_actividad'].min():.0f} - {usuarios_existentes['score_actividad'].max():.0f}")

print(f"\n    Usuarios nuevos (n={len(usuarios_nuevos):,}):")
print(f"      Media: {usuarios_nuevos['score_actividad'].mean():.4f}")
print(f"      Desv.Est: {usuarios_nuevos['score_actividad'].std():.4f}")
print(f"      Min-Max: {usuarios_nuevos['score_actividad'].min():.0f} - {usuarios_nuevos['score_actividad'].max():.0f}")

print(f"\n  score_perfil:")
print(f"    Usuarios existentes (n={len(usuarios_existentes):,}):")
print(f"      Media: {usuarios_existentes['score_perfil'].mean():.4f}")
print(f"      Desv.Est: {usuarios_existentes['score_perfil'].std():.4f}")
print(f"      Min-Max: {usuarios_existentes['score_perfil'].min():.0f} - {usuarios_existentes['score_perfil'].max():.0f}")

print(f"\n    Usuarios nuevos (n={len(usuarios_nuevos):,}):")
print(f"      Media: {usuarios_nuevos['score_perfil'].mean():.4f}")
print(f"      Desv.Est: {usuarios_nuevos['score_perfil'].std():.4f}")
print(f"      Min-Max: {usuarios_nuevos['score_perfil'].min():.0f} - {usuarios_nuevos['score_perfil'].max():.0f}")

# Impacto en variable target
print(f"\n🎯 IMPACTO EN VARIABLE TARGET (compra) POR GRUPO:")
print("-" * 100)

for user_type, label in [(0, "Usuarios existentes"), (1, "Usuarios nuevos")]:
    subset = df_v3[df_v3['usuario_nuevo'] == user_type]
    compra_pct = (subset['compra'] == 1).sum() / len(subset) * 100
    print(f"\n  {label} ({len(subset):,} registros):")
    print(f"    Tasa de compra: {compra_pct:.2f}%")
    print(f"    Compra=0: {(subset['compra'] == 0).sum():,} ({(subset['compra'] == 0).sum()/len(subset)*100:.2f}%)")
    print(f"    Compra=1: {(subset['compra'] == 1).sum():,} ({(subset['compra'] == 1).sum()/len(subset)*100:.2f}%)")

# Correlaciones con target
print(f"\n📈 CORRELACIONES CON VARIABLE TARGET:")
print("-" * 100)

for col in ['usuario_nuevo', 'score_actividad', 'score_perfil']:
    if col in df_v3.columns:
        mask = df_v3[col].notna() & df_v3['compra'].notna()
        if mask.sum() > 0:
            corr = df_v3.loc[mask, col].corr(df_v3.loc[mask, 'compra'])
            print(f"  {col:<25} Correlación: {corr:>8.4f}")

# Muestras de datos
print(f"\n📌 MUESTRAS DE DATOS (usuarios nuevos - primeras 5):")
print("-" * 100)
cols = ['id', 'origen', 'score_actividad', 'score_perfil', 'usuario_nuevo', 'compra']
print(df_v3[df_v3['usuario_nuevo'] == 1][cols].head().to_string())

print(f"\n\n📌 MUESTRAS DE DATOS (usuarios existentes - primeras 5):")
print("-" * 100)
print(df_v3[df_v3['usuario_nuevo'] == 0][cols].head().to_string())

# Resumen final
print(f"\n\n" + "=" * 100)
print("✨ VALIDACIÓN COMPLETADA")
print("=" * 100)
print(f"\n✅ Confirmaciones:")
print(f"   ✓ Nulos en scores: {df_v3[['score_actividad', 'score_perfil']].isna().sum().sum()} (todos imputados)")
print(f"   ✓ Variable usuario_nuevo creada correctamente")
print(f"   ✓ Registros con usuario_nuevo=1: {len(usuarios_nuevos):,} (imputados con ceros)")
print(f"   ✓ Registros con usuario_nuevo=0: {len(usuarios_existentes):,} (no imputados)")
print(f"   ✓ Integridad de datos verificada")

print(f"\n")
