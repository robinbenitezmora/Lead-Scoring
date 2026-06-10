import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
import cloudpickle
import warnings

warnings.filterwarnings('ignore')

# Constantes
PROJECT_ROOT = Path(__file__).parent.parent
CSV_PATH = PROJECT_ROOT / "02_datos" / "01_Originales" / "Leads.csv"
TARGET = "compra"
RANDOM_STATE = 42
ARTEFACTO_PATH = Path(__file__).parent / "artefacto_pipeline.pkl"

# Variables de agrupación (del manifiesto)
var_ohe = ['origen', 'fuente', 'ult_actividad', 'ambito', 'ocupacion', 'descarga_lm']
var_bin = ['conociste_google', 'conociste_periodico', 'conociste_facebook', 'conociste_referencias']
num_escalar = ['visitas_total', 'tiempo_en_site_total', 'paginas_vistas_visita', 'score_actividad', 'score_perfil']
var_sin_transform = ['usuario_nuevo']

variables_aisladas = ['id', 'no_enviar_email']


def prepara_datos(df):
    """Aplicar transformaciones de filas: limpieza y preparación de datos."""
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


def convertir_binarias(X):
    """Convertir variables binarias de string (Yes/No) a int (1/0)."""
    X_bin = X[var_bin].copy()
    for col in var_bin:
        if col in X_bin.columns:
            X_bin[col] = (X_bin[col] == 'Yes').astype(int)
    return X_bin


# 1. Carga y preparación de datos
print("Cargando datos...")
df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")
df = prepara_datos(df)

print(f"Registros post-limpieza: {len(df):,}")

# P05: Split train/validation (70/30 con stratificación)
train_df, validation_df = train_test_split(
    df,
    test_size=0.30,
    random_state=RANDOM_STATE,
    stratify=df.get('usuario_nuevo', df[TARGET])
)

print(f"Train: {len(train_df):,} | Validation: {len(validation_df):,}")

# Separar target y features
y_train = train_df[TARGET].copy()
X_train = train_df.drop(columns=variables_aisladas + [TARGET]).copy()

print(f"Features: {X_train.shape[1]}")

# 2. Definir transformers
# Transformer para binarias
def transform_binarias(X):
    X_copy = X.copy()
    for col in var_bin:
        if col in X_copy.columns:
            X_copy[col] = (X_copy[col] == 'Yes').astype(int)
    return X_copy

transformer_binarias = FunctionTransformer(transform_binarias, validate=False)

# 3. ColumnTransformer
preprocessor = make_column_transformer(
    (MinMaxScaler(), num_escalar),
    (OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), var_ohe),
    (transformer_binarias, var_bin),
    (FunctionTransformer(lambda x: x), var_sin_transform),
    remainder='drop'
)

# 4. Modelo base
modelo_base = LogisticRegression(
    penalty='l2',
    solver='lbfgs',
    max_iter=1000,
    random_state=RANDOM_STATE
)

# 5. Pipeline
pipe = make_pipeline(preprocessor, modelo_base)

# 6. Espacio de búsqueda de hiperparámetros
param_distributions = {
    'logisticregression__C': [0.001, 0.01, 0.1, 1, 10, 100],
}

# 7. Búsqueda de hiperparámetros con StratifiedKFold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

print("\nIniciando RandomizedSearchCV...")
search = RandomizedSearchCV(
    estimator=pipe,
    param_distributions=param_distributions,
    n_iter=30,
    cv=skf,
    scoring='roc_auc',
    n_jobs=-1,
    random_state=RANDOM_STATE,
    refit=True,
    verbose=1
)

search.fit(X_train, y_train)

print(f"\nMejor CV AUC: {search.best_score_:.4f}")
print(f"Mejores hiperparámetros: {search.best_params_}")

# 8. Obtener mejor pipeline y reentrenar con todos los datos
best_pipe = search.best_estimator_

# Evaluar en validación
X_val = validation_df.drop(columns=variables_aisladas + [TARGET]).copy()
y_val = validation_df[TARGET].copy()

y_pred_proba = best_pipe.predict_proba(X_val)[:, 1]
y_pred = best_pipe.predict(X_val)

auc_val = roc_auc_score(y_val, y_pred_proba)
acc_val = accuracy_score(y_val, y_pred)
prec_val = precision_score(y_val, y_pred)
rec_val = recall_score(y_val, y_pred)
f1_val = f1_score(y_val, y_pred)

print(f"\nMétricas en Validation Set:")
print(f"  AUC-ROC:  {auc_val:.4f}")
print(f"  Accuracy: {acc_val:.4f}")
print(f"  Precision: {prec_val:.4f}")
print(f"  Recall: {rec_val:.4f}")
print(f"  F1-Score: {f1_val:.4f}")

# 9. Serializar mejor pipeline
print(f"\nGuardando pipeline en: {ARTEFACTO_PATH}")
with open(ARTEFACTO_PATH, 'wb') as f:
    cloudpickle.dump(best_pipe, f)

print("✅ Pipeline entrenado y guardado exitosamente")
