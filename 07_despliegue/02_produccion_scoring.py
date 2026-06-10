import argparse
import pandas as pd
from pathlib import Path
import cloudpickle
import warnings

warnings.filterwarnings('ignore')

# Constantes
PROJECT_ROOT = Path(__file__).parent.parent
ARTEFACTO_PATH = Path(__file__).parent / "artefacto_pipeline.pkl"

variables_aisladas = ['id', 'no_enviar_email']
TARGET = "compra"

# Variables de agrupación (deben coincidir con reentrenamiento.py)
var_ohe = ['origen', 'fuente', 'ult_actividad', 'ambito', 'ocupacion', 'descarga_lm']
var_bin = ['conociste_google', 'conociste_periodico', 'conociste_facebook', 'conociste_referencias']
num_escalar = ['visitas_total', 'tiempo_en_site_total', 'paginas_vistas_visita', 'score_actividad', 'score_perfil']
var_sin_transform = ['usuario_nuevo']


def prepara_datos(df):
    """Aplicar transformaciones de filas: limpieza y preparación de datos.
    DEBE SER IDÉNTICA A LA FUNCIÓN EN 01_reentrenamiento.py"""
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


# Parsear argumentos
parser = argparse.ArgumentParser(
    description="Script de scoring en producción usando pipeline entrenado",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Ejemplo de uso:
  python 02_produccion_scoring.py --input datos_nuevos.csv --output resultados_scoring.csv
    """
)
parser.add_argument(
    "--input",
    type=str,
    required=True,
    help="Ruta del CSV de entrada (datos para scoring)"
)
parser.add_argument(
    "--output",
    type=str,
    required=True,
    help="Ruta del CSV de salida (con predicciones)"
)

args = parser.parse_args()

# Validar que el artefacto existe
if not ARTEFACTO_PATH.exists():
    raise FileNotFoundError(f"Artefacto no encontrado: {ARTEFACTO_PATH}\nEjecuta primero: python 01_reentrenamiento.py")

# Cargar datos nuevos
print(f"Cargando datos desde: {args.input}")
df_nuevo = pd.read_csv(args.input, sep=";", encoding="utf-8")
print(f"Registros cargados: {len(df_nuevo):,}")

# Aplicar preparación de datos (mismo flujo que en reentrenamiento)
df_nuevo = prepara_datos(df_nuevo)
print(f"Registros post-limpieza: {len(df_nuevo):,}")

# Separar ID para reinsertar después
df_ids = df_nuevo[['id']].copy() if 'id' in df_nuevo.columns else None

# Preparar features (excluir variables aisladas y target si existe)
X_nuevo = df_nuevo.drop(
    columns=[col for col in variables_aisladas + [TARGET] if col in df_nuevo.columns],
    errors='ignore'
).copy()

print(f"Features para scoring: {X_nuevo.shape[1]}")

# Cargar artefacto (pipeline entrenado)
print(f"\nCargando pipeline desde: {ARTEFACTO_PATH}")
with open(ARTEFACTO_PATH, 'rb') as f:
    pipeline = cloudpickle.load(f)

print("Pipeline cargado exitosamente")

# Generar predicciones
print("\nGenerando predicciones...")
probabilidades = pipeline.predict_proba(X_nuevo)[:, 1]
predicciones = pipeline.predict(X_nuevo)

print(f"Predicciones generadas: {len(probabilidades):,}")
print(f"Proporción de predicciones positivas: {predicciones.mean():.2%}")
print(f"Probabilidad promedio: {probabilidades.mean():.4f}")
print(f"Rango de probabilidades: [{probabilidades.min():.4f}, {probabilidades.max():.4f}]")

# Construir DataFrame de resultados
resultado = df_ids.copy() if df_ids is not None else pd.DataFrame()
resultado['prediction'] = predicciones
resultado['probability'] = probabilidades

# Guardar resultados
print(f"\nGuardando resultados en: {args.output}")
resultado.to_csv(args.output, sep=";", index=False, encoding="utf-8")

print("✅ Scoring completado exitosamente")
