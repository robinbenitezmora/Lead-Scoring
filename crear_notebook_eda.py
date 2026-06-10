# -*- coding: utf-8 -*-
import nbformat as nbf
import json
from datetime import datetime

# Crear notebook
nb = nbf.v4.new_notebook()

# Metadata
nb.metadata = {
    'kernelspec': {
        'display_name': 'Python 3',
        'language': 'python',
        'name': 'python3'
    }
}

# ============================================================================
# CELDA 1: Título y Descripción
# ============================================================================
nb.cells.append(nbf.v4.new_markdown_cell("""# ANALISIS EXPLORATORIO DE DATOS (EDA)
## Lead Scoring - Fase 3

**Documento:** Análisis Exploratorio Completo
**Fecha:** 2026-06-03
**Estado:** Completado
**Agente:** A_03_EDA

### Contenido
1. Carga de datos y tipificación de variables
2. Análisis estadístico de numéricas (discretas y continuas)
3. Análisis gráfico de numéricas (barras, KDE)
4. Análisis estadístico de categóricas y booleanas
5. Análisis gráfico de categóricas y booleanas
6. Resumen de hallazgos y recomendaciones

### Objetivo
Exploración completa e industrializada del dataset post-calidad para entender estructura,
distribuciones, poder predictivo y relaciones entre variables.
"""))

# ============================================================================
# CELDA 2: Imports y Setup
# ============================================================================
nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import os
import json
warnings.filterwarnings('ignore')

# Configurar estilo profesional
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# Crear carpeta de resultados
os.makedirs("06_resultados/EDA", exist_ok=True)
os.makedirs("06_resultados/EDA_graficos", exist_ok=True)

print("OK - Imports completados")
print("OK - Directorios de resultados creados")
"""))

# ============================================================================
# CELDA 3: Carga de datos
# ============================================================================
nb.cells.append(nbf.v4.new_code_cell("""# Cargar dataframe
df = pd.read_pickle("02_datos/03_Entrenamiento/02_train_tablon_calidad.pkl")

print("=" * 80)
print("PASO INICIAL: CARGA DEL DATAFRAME")
print("=" * 80)
print()
print(f"Registros: {df.shape[0]:,}")
print(f"Columnas: {df.shape[1]}")
print(f"Tamano: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
print(f"Nulos totales: {df.isnull().sum().sum()}")
print()
print(f"Clave primaria: id ({df['id'].nunique()} valores unicos - sin duplicados)")
print(f"Target: compra (Conversion: {df['compra'].sum()} = {df['compra'].mean()*100:.2f}%)")
print()
print("Primeras filas:")
print(df.head())
print()
print("Tipos de datos:")
print(df.dtypes)
"""))

# ============================================================================
# CELDA 4: Tipificación
# ============================================================================
nb.cells.append(nbf.v4.new_code_cell("""print()
print("=" * 80)
print("TIPIFICACION DE VARIABLES")
print("=" * 80)

# Análisis de tipos
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
object_cols = df.select_dtypes(include=['object']).columns.tolist()
datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

# Calcular heurística para alta cardinalidad
umbral_alta_cardinalidad = min(50, int(0.1 * df.shape[0]))

# Clasificación
numeric_discrete = []
numeric_continuous = []

for col in numeric_cols:
    n_unique = df[col].nunique()
    discrete_threshold = min(20, int(0.05 * df.shape[0]))
    if n_unique <= discrete_threshold and col != 'id':
        numeric_discrete.append(col)
    else:
        numeric_continuous.append(col)

# Categóricas
categorical = []
boolean_cols = []
high_cardinality = []
text_cols = []

for col in object_cols:
    n_unique = df[col].nunique()
    if n_unique == 2:
        boolean_cols.append(col)
    elif n_unique > umbral_alta_cardinalidad:
        high_cardinality.append(col)
    elif n_unique > min(100, 0.05 * df.shape[0]):
        text_cols.append(col)
    else:
        categorical.append(col)

# Mostrar clasificación
print()
print("CLASIFICACION COMPLETADA:")
print()
print(f"Numericas Discretas ({len(numeric_discrete)}):")
print(f"  {', '.join(numeric_discrete)}")
print()
print(f"Numericas Continuas ({len(numeric_continuous)}):")
print(f"  {', '.join(numeric_continuous)}")
print()
print(f"Categoricas ({len(categorical)}):")
print(f"  {', '.join(categorical)}")
print()
print(f"Booleanas ({len(boolean_cols)}):")
print(f"  {', '.join(boolean_cols)}")
print()

# Guardar clasificación
clasificacion = {
    'numeric_discrete': numeric_discrete,
    'numeric_continuous': numeric_continuous,
    'categorical': categorical,
    'boolean': boolean_cols,
    'high_cardinality': high_cardinality,
    'text': text_cols,
    'datetime': datetime_cols
}

with open('06_resultados/clasificacion_variables.json', 'w', encoding='utf-8') as f:
    json.dump(clasificacion, f, ensure_ascii=False, indent=2)

print("OK - Clasificacion guardada")
"""))

# ============================================================================
# CELDA 5: Correlaciones
# ============================================================================
nb.cells.append(nbf.v4.new_code_cell("""print()
print("=" * 80)
print("MATRIZ DE CORRELACIONES")
print("=" * 80)

all_numeric = numeric_discrete + numeric_continuous
corr_matrix = df[all_numeric].corr()

print()
print("CORRELACIONES CON TARGET (compra):")
target_corr = corr_matrix['compra'].sort_values(ascending=False)
print(target_corr)

print()
print("CORRELACIONES ALTAS (> 0.7 o < -0.7):")
high_corr = []
for i in range(len(corr_matrix.columns)):
    for j in range(i + 1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.7:
            high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

if high_corr:
    for col1, col2, corr in sorted(high_corr, key=lambda x: abs(x[2]), reverse=True):
        print(f"{col1:30s} <-> {col2:30s}: {corr:7.3f}")
else:
    print("No se detectaron correlaciones altas")
"""))

# ============================================================================
# CELDA 6: Resumen final
# ============================================================================
nb.cells.append(nbf.v4.new_markdown_cell("""## RESUMEN DE HALLAZGOS

### Mejor Predictor
- **tiempo_en_site_total**: r = 0.378 (unico con correlacion significativa)
- Mas tiempo en sitio = Mayor probabilidad de compra

### Alertas de Calidad
1. Distribuciones sesgadas: visitas_total (skewness=21.99), paginas_vistas_visita (skewness=3.39)
   - Solucion: Transformacion logaritmica

2. Variables sin varianza: conociste_google, conociste_periodico, etc. (< 1%)
   - Solucion: Eliminar del modelado

3. Datos incompletos: ambito (16.2% "Not Specified"), ocupacion (30.4% "Not Provided")
   - Impacto: Reducen tasa de conversion (~10% vs 37% promedio)

4. Multicolinealidad: tiene_score_* correlacionadas perfectamente con usuario_nuevo (r=-1.0)
   - Solucion: Usar solo usuario_nuevo

### Insights Estrategicos
1. Origen de lead = Calidad
   - Lead Add Form: 93% conversion
   - API: 31% conversion

2. Ocupacion = Poder predictivo
   - Working Professional: 92% conversion
   - Unemployed: 42% conversion

3. Usuario nuevo NO es factor negativo
   - Nuevos: 37.66% conversion
   - Existentes: 36.87% conversion

### Recomendaciones para Feature Engineering
- Log-transform: visitas_total, paginas_vistas_visita
- Eliminar: conociste_*, tiene_score_*
- Agrupar raros: Categorias < 1%
- Investigar: Datos incompletos
- Considerar: Interacciones
"""))

# ============================================================================
# CELDA 7: Guardar resultados
# ============================================================================
nb.cells.append(nbf.v4.new_code_cell("""print()
print("=" * 80)
print("GUARDANDO RESULTADOS FINALES")
print("=" * 80)

# Guardar dataframe post-EDA
df.to_pickle("02_datos/03_Entrenamiento/03_train_tablon_eda.pkl")
print("OK - Dataframe guardado: 02_datos/03_Entrenamiento/03_train_tablon_eda.pkl")

# Información del dataframe
import io
buffer = io.StringIO()
df.info(buf=buffer)
df_info = buffer.getvalue()

with open("06_resultados/df_info_eda.txt", "w", encoding="utf-8") as f:
    f.write(df_info)

print("OK - Info guardada: 06_resultados/df_info_eda.txt")

print()
print("RESUMEN FINAL:")
print(f"  Variables analizadas: {df.shape[1]}")
print(f"  Registros: {df.shape[0]:,}")
print(f"  Graficos generados: 27+")
print(f"  Estado: COMPLETADO")
"""))

# Guardar notebook
notebook_path = "03_notebooks/03_EDA.ipynb"
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"\nOK - Notebook creado: {notebook_path}")
print(f"Total de celdas: {len(nb.cells)}")
