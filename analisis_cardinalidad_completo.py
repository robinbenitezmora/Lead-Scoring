import pandas as pd
import json
import numpy as np

# Cargar datos
df = pd.read_csv(
    r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean.csv',
    sep=';'
)

print("=" * 100)
print("ANÁLISIS COMPLETO DE CARDINALIDAD Y DISTRIBUCIONES")
print("=" * 100)

# Análisis de cardinalidad
print("\n📊 ANÁLISIS DE CARDINALIDAD\n")
print(f"{'Columna':<25} {'Tipo':<12} {'Únicos':<8} {'% Cobertura':<12} {'Faltantes':<12} {'Nota'}")
print("-" * 100)

analisis_cardinalidad = {}

for col in df.columns:
    dtype = df[col].dtype
    n_unique = df[col].nunique()
    n_missing = df[col].isna().sum()
    pct_unique = (n_unique / len(df)) * 100
    pct_missing = (n_missing / len(df)) * 100

    # Clasificación
    if dtype in ['int64', 'float64']:
        if n_unique == 2 and set(df[col].dropna().unique()).issubset({0, 1, 0.0, 1.0}):
            tipo = 'Booleana'
        else:
            tipo = 'Numérica'
    else:
        tipo = 'Categórica'

    # Nota especial
    nota = ""
    if n_missing > 0:
        nota += f"Faltantes: {n_missing}"
    if n_unique == 1:
        nota += " | ÚNICA CATEGORÍA" if nota else "ÚNICA CATEGORÍA"
    if pct_unique > 90:
        nota += " | Alta variedad" if nota else "Alta variedad"

    print(f"{col:<25} {tipo:<12} {n_unique:<8} {pct_unique:<12.2f}% {pct_missing:<12.2f}% {nota}")

    analisis_cardinalidad[col] = {
        'tipo': tipo,
        'unicos': int(n_unique),
        'pct_unique': round(pct_unique, 2),
        'faltantes': int(n_missing),
        'pct_faltantes': round(pct_missing, 2)
    }

# Análisis de valores por categoría para variables categóricas
print("\n\n" + "=" * 100)
print("DISTRIBUCIÓN DE CATEGORÍAS (Top valores)")
print("=" * 100)

for col in df.columns:
    if df[col].dtype == 'object' and df[col].nunique() <= 30:
        print(f"\n📋 {col}")
        print("-" * 50)
        value_counts = df[col].value_counts()
        total = len(df) - df[col].isna().sum()

        for val, count in value_counts.head(10).items():
            pct = (count / total) * 100
            bar_length = int(pct / 2)
            bar = "█" * bar_length
            print(f"  {str(val):<30} {count:>6} ({pct:>6.2f}%) {bar}")

        if len(value_counts) > 10:
            otros = value_counts[10:].sum()
            pct_otros = (otros / total) * 100
            print(f"  {'[Otros]':<30} {otros:>6} ({pct_otros:>6.2f}%)")

# Análisis estadístico de variables numéricas
print("\n\n" + "=" * 100)
print("ESTADÍSTICAS DE VARIABLES NUMÉRICAS")
print("=" * 100)

for col in df.columns:
    if df[col].dtype in ['int64', 'float64'] and df[col].nunique() > 2:
        print(f"\n📈 {col}")
        print("-" * 50)
        stats = df[col].describe()

        print(f"  Recuento:    {int(stats['count'])}")
        print(f"  Media:       {stats['mean']:.4f}")
        print(f"  Mediana:     {df[col].median():.4f}")
        print(f"  Desv. Est:   {stats['std']:.4f}")
        print(f"  Min:         {stats['min']:.4f}")
        print(f"  Max:         {stats['max']:.4f}")
        print(f"  Q1 (25%):    {stats['25%']:.4f}")
        print(f"  Q3 (75%):    {stats['75%']:.4f}")
        print(f"  Rango:       {stats['max'] - stats['min']:.4f}")
        print(f"  Faltantes:   {df[col].isna().sum()} ({(df[col].isna().sum() / len(df) * 100):.2f}%)")

# Correlación de variables booleanas con target
print("\n\n" + "=" * 100)
print("CORRELACIÓN CON VARIABLE TARGET (compra)")
print("=" * 100)

if 'compra' in df.columns:
    print(f"\n{'Columna':<25} {'Correlación':<15} {'Nota'}")
    print("-" * 60)

    for col in df.columns:
        if col != 'compra' and df[col].dtype in ['int64', 'float64']:
            # Calcular solo para filas sin NaN
            mask = df[col].notna() & df['compra'].notna()
            if mask.sum() > 0:
                corr = df.loc[mask, col].corr(df.loc[mask, 'compra'])
                abs_corr = abs(corr)

                if abs_corr > 0.3:
                    nota = "FUERTE"
                elif abs_corr > 0.15:
                    nota = "MODERADA"
                elif abs_corr > 0.05:
                    nota = "DÉBIL"
                else:
                    nota = "Muy débil"

                print(f"{col:<25} {corr:>10.4f}      {nota}")

# Guardar reporte en JSON
reporte = {
    'fecha_analisis': pd.Timestamp.now().isoformat(),
    'estadisticas_generales': {
        'registros': len(df),
        'columnas': len(df.columns),
        'columnas_numericas': len([c for c in df.columns if df[c].dtype in ['int64', 'float64']]),
        'columnas_categoricas': len([c for c in df.columns if df[c].dtype == 'object'])
    },
    'cardinalidad': analisis_cardinalidad
}

output_path = r'c:\Users\robin\dev\01_LEADSCORING\06_resultados\03_reporte_cardinalidad.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(reporte, f, indent=2, ensure_ascii=False)

print(f"\n\n✅ Reporte guardado en: {output_path}")
