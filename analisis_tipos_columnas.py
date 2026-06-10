import pandas as pd
import json

# Cargar datos
df = pd.read_csv(
    r'c:\Users\robin\dev\01_LEADSCORING\02_datos\03_Entrenamiento\df_leads_clean.csv',
    sep=';'
)

# Cargar EDA actual
with open(r'c:\Users\robin\dev\01_LEADSCORING\06_resultados\01_eda_summary.json') as f:
    eda_actual = json.load(f)

print("=" * 80)
print("ANÁLISIS DETALLADO DE TIPOS DE COLUMNAS")
print("=" * 80)
print(f"\nDatos: {df.shape[0]} registros, {df.shape[1]} columnas\n")

# Crear análisis detallado
analisis_detallado = {}

for col in df.columns:
    dtype = df[col].dtype
    n_unique = df[col].nunique()
    n_missing = df[col].isna().sum()
    pct_missing = (n_missing / len(df)) * 100

    # Detectar tipo
    if col == 'id':
        tipo_detectado = 'identificador'
    elif dtype in ['float64', 'int64']:
        # Podría ser numérica, booleana o categórica
        if n_unique == 2 and set(df[col].dropna().unique()).issubset({0, 1, 0.0, 1.0}):
            tipo_detectado = 'booleana (0/1)'
        elif n_unique <= 20 and dtype == 'int64':
            tipo_detectado = 'categórica (numérica)'
        else:
            tipo_detectado = 'numérica'
    else:  # object
        # Podría ser categórica o texto
        avg_length = df[col].astype(str).str.len().mean()
        if n_unique <= 50:
            tipo_detectado = 'categórica'
        elif avg_length > 50:
            tipo_detectado = 'texto'
        else:
            tipo_detectado = 'categórica'

    # Clasificación actual
    en_eda = False
    clasificacion_actual = None
    if col in eda_actual['variables_numericas']:
        clasificacion_actual = 'numérica'
        en_eda = True
    elif col in eda_actual['variables_categoricas']:
        clasificacion_actual = 'categórica'
        en_eda = True

    # Almacenar análisis
    analisis_detallado[col] = {
        'dtype_pandas': str(dtype),
        'tipo_detectado': tipo_detectado,
        'clasificacion_en_eda': clasificacion_actual,
        'valores_unicos': n_unique,
        'valores_faltantes': n_missing,
        'pct_faltantes': round(pct_missing, 2),
        'en_eda': en_eda,
        'ejemplos': list(df[col].dropna().unique()[:5]) if n_unique <= 10 else None
    }

# Imprimir análisis
print("ANÁLISIS POR COLUMNA:")
print("-" * 80)

columnas_faltantes = []
cambios_recomendados = []

for col, info in analisis_detallado.items():
    print(f"\n📊 {col}")
    print(f"   Tipo Pandas: {info['dtype_pandas']}")
    print(f"   Tipo Detectado: {info['tipo_detectado']}")
    print(f"   Valores únicos: {info['valores_unicos']}")
    print(f"   Valores faltantes: {info['valores_faltantes']} ({info['pct_faltantes']}%)")

    if info['en_eda']:
        print(f"   ✓ En EDA como: {info['clasificacion_en_eda']}")
    else:
        print(f"   ⚠️  NO ESTÁ EN EDA")
        columnas_faltantes.append(col)

    if info['clasificacion_en_eda'] and info['tipo_detectado'] != info['clasificacion_en_eda']:
        if not (info['tipo_detectado'] == 'categórica (numérica)' and info['clasificacion_en_eda'] == 'categórica'):
            print(f"   ⚠️  Posible discrepancia: detectado={info['tipo_detectado']}, EDA={info['clasificacion_en_eda']}")
            cambios_recomendados.append({
                'columna': col,
                'detectado': info['tipo_detectado'],
                'en_eda': info['clasificacion_en_eda']
            })

    if info['ejemplos']:
        print(f"   Ejemplos: {info['ejemplos']}")

# Resumen
print("\n" + "=" * 80)
print("RESUMEN Y RECOMENDACIONES")
print("=" * 80)

if columnas_faltantes:
    print(f"\n⚠️  COLUMNAS NO CLASIFICADAS EN EDA:")
    for col in columnas_faltantes:
        info = analisis_detallado[col]
        print(f"   • {col} → Tipo: {info['tipo_detectado']}, Únicos: {info['valores_unicos']}")

if cambios_recomendados:
    print(f"\n⚠️  POSIBLES CAMBIOS DE CLASIFICACIÓN:")
    for item in cambios_recomendados:
        print(f"   • {item['columna']}: {item['en_eda']} → {item['detectado']}")

# Estadísticas generales
print(f"\n📈 ESTADÍSTICAS GENERALES:")
n_numericas = len([c for c in analisis_detallado.values() if c['clasificacion_en_eda'] == 'numérica'])
n_categoricas = len([c for c in analisis_detallado.values() if c['clasificacion_en_eda'] == 'categórica'])
n_sin_clasificar = len(columnas_faltantes)

print(f"   • Variables numéricas en EDA: {n_numericas}")
print(f"   • Variables categóricas en EDA: {n_categoricas}")
print(f"   • Variables sin clasificar: {n_sin_clasificar}")
print(f"   • Total variables: {len(analisis_detallado)}")

# Guardar análisis detallado
output_path = r'c:\Users\robin\dev\01_LEADSCORING\06_resultados\02_analisis_tipos_detallado.json'
with open(output_path, 'w', encoding='utf-8') as f:
    # Convertir ejemplos a strings para JSON
    analisis_json = {}
    for col, info in analisis_detallado.items():
        info_copy = info.copy()
        if info_copy['ejemplos']:
            info_copy['ejemplos'] = [str(x) for x in info_copy['ejemplos']]
        # Convertir valores numpy a tipos nativos de Python
        info_copy['valores_unicos'] = int(info_copy['valores_unicos'])
        info_copy['valores_faltantes'] = int(info_copy['valores_faltantes'])
        analisis_json[col] = info_copy
    json.dump(analisis_json, f, indent=2, ensure_ascii=False)

print(f"\n✅ Análisis detallado guardado en: {output_path}")
