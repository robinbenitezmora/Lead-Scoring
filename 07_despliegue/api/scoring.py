"""
Motor de scoring reutilizable extraído del flujo real de 02_produccion_scoring.py.

Función principal: scoring_df(df) → DataFrame con predicciones

Input: DataFrame con 16 features (después de normalización)
Output: DataFrame con columnas [id, prediction, probability]
"""

import pandas as pd
from pathlib import Path
import cloudpickle
import warnings

warnings.filterwarnings('ignore')

# Resolución de rutas (compatible con local y Render)
BASE_DIR = Path(__file__).parent
ARTEFACTO_PATH = BASE_DIR / "artefacto_pipeline.pkl"

# Configuración de variables (idéntica a 02_produccion_scoring.py)
variables_aisladas = ['id', 'no_enviar_email']
TARGET = "compra"

var_ohe = ['origen', 'fuente', 'ult_actividad', 'ambito', 'ocupacion', 'descarga_lm']
var_bin = ['conociste_google', 'conociste_periodico', 'conociste_facebook', 'conociste_referencias']
num_escalar = ['visitas_total', 'tiempo_en_site_total', 'paginas_vistas_visita', 'score_actividad', 'score_perfil']
var_sin_transform = ['usuario_nuevo']


def prepara_datos(df):
    """
    Aplicar transformaciones de filas: limpieza y preparación de datos.
    IDÉNTICA a la función en 02_produccion_scoring.py
    """
    df = df.copy()

    # P02: Eliminar nulos críticos
    columnas_criticas = ['visitas_total', 'paginas_vistas_visita']
    mask_nulos = df[columnas_criticas].isna().any(axis=1)
    df = df[~mask_nulos].reset_index(drop=True)

    # P03: Imputar scores y crear usuario_nuevo
    columnas_scores = ['score_actividad', 'score_perfil']
    mask_ambos_nulos = df[columnas_scores].isna().all(axis=1)
    df['usuario_nuevo'] = 0
    df.loc[mask_ambos_nulos, 'usuario_nuevo'] = 1
    df[columnas_scores] = df[columnas_scores].fillna(0)

    # P04: Imputar categóricas
    df['fuente'] = df['fuente'].fillna('Unknown')
    df['ambito'] = df['ambito'].fillna('Not Specified')
    df['ocupacion'] = df['ocupacion'].fillna('Not Provided')

    # Eliminar columnas sin varianza
    df = df.drop(columns=['conociste_revista', 'conociste_youtube', 'no_llamar'], errors='ignore')

    return df


def scoring_df(df):
    """
    Motor de scoring: recibe DataFrame y devuelve predicciones.

    Input:
      df (DataFrame): Datos para scoring (puede venir con más columnas, será normalizado)

    Output:
      DataFrame: Columnas [id, prediction, probability]
        - id: identificador único
        - prediction: 0 o 1 (predicción binaria)
        - probability: float [0.0, 1.0] (probabilidad de compra)

    Pasos:
      1. Copiar entrada
      2. Aplicar prepara_datos (normalización, imputación, eliminación low-variance)
      3. Preservar id
      4. Seleccionar features
      5. Cargar artefacto
      6. Generar predicciones
      7. Construir salida
    """
    # 1. Copiar entrada
    df = df.copy()

    # 2. Aplicar preparación (normalización + transformaciones)
    df = prepara_datos(df)

    # 3. Preservar ID para reinsertar después
    df_ids = df[['id']].copy() if 'id' in df.columns else None

    # 4. Seleccionar features (excluir variables aisladas + target si existe)
    X = df.drop(
        columns=[col for col in variables_aisladas + [TARGET] if col in df.columns],
        errors='ignore'
    ).copy()

    # 5. Cargar artefacto (pipeline entrenado)
    if not ARTEFACTO_PATH.exists():
        raise FileNotFoundError(
            f"Artefacto no encontrado: {ARTEFACTO_PATH}\n"
            f"Verifica que exista el archivo serializado del modelo."
        )

    with open(ARTEFACTO_PATH, 'rb') as f:
        pipeline = cloudpickle.load(f)

    # 6. Generar predicciones
    probabilidades = pipeline.predict_proba(X)[:, 1]
    predicciones = pipeline.predict(X)

    # 7. Construir salida
    resultado = df_ids.copy() if df_ids is not None else pd.DataFrame()
    resultado['prediction'] = predicciones.astype(int)
    resultado['probability'] = probabilidades

    return resultado
