# 🚀 Copilot Instructions - Lead Scoring Project

**Última Actualización:** 2026-06-09  
**Estado del Proyecto:** Fase 7 ✅ + Fase 8 ✅ + Fase 9 ✅ (PIPELINES A_09 COMPLETADA) → **LISTO PARA EJECUCIÓN Y FASE 10: VALIDACIÓN**

---

## 📌 CONTEXTO DEL PROYECTO

### Objetivo General
Construir un modelo de **Lead Scoring** que prediga probabilidad de conversión (compra) basado en comportamiento y características demográficas.

### Dataset Principal
- **Archivo Base:** `df_leads_clean_v3.csv` ⚠️ **USAR ESTA VERSIÓN**
- **Registros:** 8,970
- **Variables:** 24 (10 numéricas, 14 categóricas)
- **Target:** `compra` (0=No compró, 1=Compró)
- **Tasa Base:** ~37% de conversión

### Versiones de Dataset
```
v1: Original con nulos (9,093 registros)
v2: Post-limpieza (8,970 registros, nulos críticos eliminados)
v3: Final ⭐ (8,970 registros, scores imputados, usuario_nuevo creado)
```

---

## 🎯 FASES DEL PROYECTO

### ✅ COMPLETADAS

#### Fase 1: Exploración e Importación
- [x] Carga y exploración inicial de datos
- [x] Identificación de problemas de calidad
- [x] Análisis de valores faltantes

#### Fase 2: Calidad de Datos
- [x] **FASE 1 - Limpieza:** Eliminación de 123 registros con nulos en visitas_total, paginas_vistas_visita (8,970 registros retenidos, 98.65%)
- [x] **FASE 2 - Imputación:** Scores imputados con cero para 4,103 usuarios nuevos (45.74%)
- [x] **Segmentación:** Variable usuario_nuevo creada (0=existente, 1=nuevo)
- [x] **Documentación:** INFORME_CALIDAD_DATOS.md
- [x] **Notebooks:** `02_Calidad_Datos.ipynb` + `01_Importacion_Datos.ipynb` (v3 disponible)

### ✅ COMPLETADAS (CONT.)

#### Fase 3: Análisis Exploratorio Actualizado ✨ NUEVO
- [x] **Análisis estadístico completo (7 tareas):** Tipificación, numéricas discretas, continuas, categóricas, booleanas, alta cardinalidad, texto/fecha
- [x] **Generación de 27 gráficos profesionales:** Distribuciones, correlaciones, conversión, interacciones
- [x] **Identificación de poder predictivo:** tiempo_en_site_total es mejor predictor (r=0.378)
- [x] **Alertas de calidad:** Variables sin varianza, distribuciones sesgadas, datos incompletos
- [x] **Análisis de alta cardinalidad:** Umbral 15+ categorías con índice Herfindahl
- [x] **Análisis de texto y fecha:** Verificación y preparación de variables especiales
- [x] **Documentación:** EDA_report.md con 50+ páginas de análisis
- [x] **Informe:** `06_resultados/EDA/EDA_report.md`

### ⏳ PRÓXIMAS FASES

#### ✅ Fase 4: Preparación de Datos (COMPLETADA)
- [x] **Transformaciones numéricas:** MinMaxScaler [0,1] para 5 variables
- [x] **OneHotEncoding:** 6 categorías → 60 dummies
- [x] **Variables aisladas:** id + no_enviar_email separadas
- [x] **Archivos generados:**
  - `02_datos/03_Entrenamiento/04_train_tablon_transformado.pkl` (6,279 × 67)
  - `02_datos/03_Entrenamiento/04_train_variables_aisladas.pkl` (6,279 × 2)

#### ✅ Fase 5: Preselección de Variables (COMPLETADA)
- [x] **Método principal:** RFECV con Regresión Logística L1
- [x] **Reducción:** 66 features → 26 features (-60.6% reducción)
- [x] **Desduplicación inteligente:** Eliminación de variables correlacionadas con usuario_nuevo
- [x] **Análisis de correlaciones:** Identificación de pares altamente correlacionados
- [x] **Archivos generados:**
  - `02_datos/03_Entrenamiento/05_train_tablon_preseleccion.pkl` (6,279 × 27, incluye target)
  - `01_Documentos/Variables_preseleccionadas.txt` (lista de 26 variables)

#### ⏭️ Fase 6: Balanceo de Clases (SALTADA)
- ⊘ **Decisión del Proyecto:** NO se aplicará balanceo de clases en este proyecto
- ⊘ **Justificación:** La distribución balanceada (37% conversión) es representativa del caso real
- ⊘ **Target:** Mantener distribución natural para predicciones en producción
- ⊘ **Dataset:** Se continúa con 6,279 registros sin modificar

#### ✅ Fase 7: Modelización (COMPLETADA - 2026-06-09) ✨ CONSOLIDADO
- [x] **Método:** Validación Cruzada 5-Fold Estratificado + Entrenamiento en Todo el Dataset
- [x] **Logistic Regression L2 SELECCIONADO:** AUC = **0.8898** (Dataset entrenamiento completo) ⭐
  - CV AUC mean: 0.8864 ± 0.0031 (5-fold) 
  - Accuracy: 82.00%, Precision: 79.01%, Recall: 70.28%, F1: 0.7439
  - Overfitting: Mínimo (diferencia 0.0034)
  - **Hiperparámetros:** C=100.0, solver='lbfgs', max_iter=1000, tol=0.0001
- [x] **Análisis Interpretabilidad (SOLO COEFICIENTES):** ✅
  - Top 10 coeficientes (dirección de impacto: + ó -)
  - Variable más predictiva: tiempo_en_site_total_mms (+1.096)
  - ⚠️ **NO se usó Permutation Importance** (por restricción de proyecto)
- [x] **Análisis de Umbrales:** 5 puntos evaluados (0.3-0.7), umbral 0.5 recomendado
- [x] **Visualizaciones:** Curva ROC + Matriz de Confusión (PNG 300 DPI)
- [x] **Artefactos generados:**
  - Notebook: `03_notebooks/06_Modelizacion.ipynb` (10 PASOS, código production-ready)
  - Configuración: `06_resultados/Modelizacion/config_mejor_modelo.json`
  - Resultados: `resultados_cv.csv`, `analisis_umbrales.csv`
  - Visualización: `roc_curve.png` (254 KB)
- ⚠️ **NOTA CRÍTICA:** Estas métricas son de CV + entrenamiento. **Evaluación FINAL** será en FASE 8 con `validation.pkl`

#### ✅ Fase 8: Pre-Producción e Integración (A_08_PreProduccionLimpieza - COMPLETADA 2026-06-09)
- [x] **PASO 0 - Mapeo del Proyecto:**
  - [x] Identificación de estructura de carpetas
  - [x] Localización de CSV original: `02_datos/01_Originales/Leads.csv` (9,093 registros)
  - [x] Auditoría de notebooks A_01..A_07
  
- [x] **PASO 1 - Integración Lineal:**
  - [x] Extracción de código transformador REAL de A_01..A_07
  - [x] Compilación en notebook centralizado `03_notebooks/08_Preproduccion.ipynb`
  - [x] Pipeline: CSV → Limpieza → Imputación → Preparación → Preselección → Modelización
  - [x] **SIN pseudo-código, SIN ejemplos** - Solo código ejecutable real
  
- [x] **PASO 2 - Limpieza y Enfoque:**
  - [x] Eliminación de análisis exploratorio (EDA removido, solo datos)
  - [x] Preservación de variables de agrupación: `var_ohe`, `var_bin`, `num_escalar`
  - [x] Preservación de train_test_split y GridSearch (requerido por A_09)
  - [x] Verificación: Modelo final = Logistic Regression L2 (AUC 0.8898)
  
- [x] **PASO 3 - Generación de Artefactos:**
  - [x] `03_notebooks/08_Preproduccion.ipynb` - Notebook integrado y limpio (ejecutable)
  - [x] `07_despliegue/pre-produccion/00_resumen_limpieza.md` - Auditoría legible
  - [x] `07_despliegue/pre-produccion/00_manifiesto_preproduccion.json` - Contrato máquina-legible para A_09

#### ✅ Fase 9: Generación de Pipelines sklearn (A_09_PreProduccion_Codigos - COMPLETADA 2026-06-09) ✨
- [x] **PASO 1 - Análisis Estático:**
  - [x] Lectura del notebook integrado `03_notebooks/08_Preproduccion.ipynb`
  - [x] Lectura del manifiesto `07_despliegue/pre-produccion/00_manifiesto_preproduccion.json`
  - [x] Extracción de variables de agrupación: var_ohe, var_bin, num_escalar, var_sin_transform
  - [x] Extracción de parámetros de búsqueda: C ∈ [0.001, 0.01, 0.1, 1, 10, 100]

- [x] **PASO 2 - Generación de Scripts:**
  - [x] `07_despliegue/01_reentrenamiento.py`:
    - [x] Pipeline sklearn: ColumnTransformer (MinMaxScaler + OneHotEncoder + FunctionTransformer)
    - [x] RandomizedSearchCV(n_iter=30, cv=StratifiedKFold(5), scoring='roc_auc')
    - [x] Búsqueda de hiperparámetro C sobre pipeline completo
    - [x] Serialización con cloudpickle → `artefacto_pipeline.pkl`
    - [x] Flujo lineal sin main() ni if __name__ == "__main__"
  - [x] `07_despliegue/02_produccion_scoring.py`:
    - [x] Carga de artefacto_pipeline.pkl
    - [x] Argumentos CLI: --input (datos nuevos) --output (resultados)
    - [x] Prepara_datos() idéntica a reentrenamiento.py
    - [x] predict_proba() para scoring
    - [x] CSV output: id + prediction + probability
    - [x] Flujo lineal sin main() ni if __name__ == "__main__"

- [x] **PASO 3 - Validación Estática:**
  - [x] 01_reentrenamiento.py: ✅ make_column_transformer, make_pipeline, RandomizedSearchCV, NO main()
  - [x] 02_produccion_scoring.py: ✅ cloudpickle.load, predict/predict_proba, NO fit, NO main()
  - [x] Documentación: `07_despliegue/pre-produccion/01_resumen_generacion_pipelines.md`

#### 🔜 Fase 10: Evaluación Final en Validation.pkl + Scoring y Ranking
- [ ] **PASO 1 - Ejecutar Reentrenamiento:**
  - [ ] `python 07_despliegue/01_reentrenamiento.py`
  - [ ] Verificar que genera `artefacto_pipeline.pkl`
  - [ ] Validar métricas en validation set
- [ ] **PASO 2 - Evaluación Final (CRÍTICO):**
  - [ ] Cargar modelo entrenado desde artefacto
  - [ ] Cargar `02_datos/02_Validacion/validation.pkl` (2,691 registros)
  - [ ] Generar predicciones sobre validation set
  - [ ] Calcular métricas finales (AUC, Precision, Recall, F1, Accuracy)
  - [ ] Documentar: ¿Generaliza bien? ¿Hay degradación vs CV?
  - [ ] Validar coeficientes (compararlos con CV)
- [ ] **PASO 3 - Scoring y Ranking:**
  - [ ] `python 07_despliegue/02_produccion_scoring.py --input datos_nuevos.csv --output predicciones.csv`
  - [ ] Merge de predicciones con variables aisladas (por `id`)
  - [ ] Aplicación de lógica de exclusión (no_enviar_email = 'No')
  - [ ] Ranking de leads por probabilidad de conversión (usar umbral 0.5)
  - [ ] Generación de reportes finales
- [ ] **PASO 4 - Exportación:**
  - [ ] Exportar leads calificados en CSV/Excel
  - [ ] Incluir: id, probabilidad, label, ranking, exclusiones

---

## 📊 VARIABLES CLAVE

### Target
- **compra:** 0=No compró (63%), 1=Compró (37%)

### Variables Críticas (Sin Imputar)
```
usuario_nuevo:              0=Usuario existente, 1=Usuario nuevo (IMPUTA)
visitas_total:              Número de visitas (sin nulos desde v2)
tiempo_en_site_total:       Segundos en sitio
paginas_vistas_visita:      Páginas promedio por visita (sin nulos desde v2)
```

### Variables Imputadas en v3
```
score_actividad:            Imputado con 0 si usuario_nuevo=1
score_perfil:               Imputado con 0 si usuario_nuevo=1
```

### Variables Categóricas (Post-EDA Agrupamiento)
```
origen:         Cómo llegó el lead (4 categorías: Landing Page 54%, API 40%, Lead Add Form 5%, Lead Import 0.4%)
fuente:         Canal de tráfico (5 categorías: Google 32%, Direct Traffic 28%, Chat 19%, Organic Search 13%, Otros 7%)
ult_actividad:  Última acción registrada (8 principales + Otros: Email Opened 37%, SMS Sent 30%, Chat 11%, Page Visited 7%, otras <3%)
ambito:         Ámbito profesional (20 categorías: Select 19%, Not Specified 16%, Finance 11%, HR 9%, Marketing 9%, otros)
ocupacion:      Ocupación del usuario (7 categorías: Unemployed 59%, Not Provided 30%, Working Prof 8%, Student 2%, otros)
conociste_*:    Variables binarias de canales (ELIMINADAS en limpieza: sin varianza)
descarga_lm:    Descargó lead magnet (Yes/No: 32% descargaron)
no_enviar_email: Preferencia no contacto email (Yes/No: 8% no enviar)
```

---

## 🔍 CARACTERÍSTICAS IMPORTANTES DEL DATASET

### Segmentación de Usuarios
```
Usuarios Existentes (usuario_nuevo=0): 4,867 (54.26%)
  • Tienen scores de actividad y perfil
  • Media score_actividad: 14.31
  • Media score_perfil: 16.35
  • Tasa conversión: 36.72%

Usuarios Nuevos (usuario_nuevo=1): 4,103 (45.74%)
  • Sin historial (scores = 0)
  • Imputados en Fase 2
  • Tasa conversión: 37.66%
```

### Distribución de Datos
- Sin valores faltantes críticos
- Distribución balanceada de conversión
- Múltiples canales de adquisición

---

## 📊 ESTADO ACTUAL DEL PROYECTO (Post FASE 7: MODELIZACIÓN COMPLETADA ✅ 2026-06-09)

### 🎯 Modelo Ganador: Logistic Regression

**Archivo de Configuración:** `06_resultados/Modelizacion/config_mejor_modelo.json`

**Métrica Principal:**
- **AUC-ROC: 0.8898** (Dataset completo) ⭐ **SUPERA OBJETIVO 0.85 ✅**
- CV AUC mean: 0.8864 ± 0.0031 (5-fold estratificado)
- Overfitting: Mínimo (0.0034 diferencia entre CV y predicción final)

**Métricas Detalladas (Threshold=0.5):**
- Accuracy:  0.8200 (82.00%)
- Precision: 0.7901 (79.01%)
- Recall:    0.7028 (70.28%)
- F1-Score:  0.7439

**Matriz de Confusión:**
- TN=3,508 | FP=436
- FN=694   | TP=1,641

### 📊 Análisis de Umbrales de Decisión:

| Umbral | Precision | Recall | F1-Score | Accuracy | Recomendación |
|--------|-----------|--------|----------|----------|---------------|
| 0.3    | 0.6798    | 0.8338 | 0.7490   | 0.7922   | 🔴 Alto Recall, bajo Precision |
| 0.4    | 0.7437    | 0.7790 | 0.7609   | 0.8180   | 🟡 Equilibrio moderado |
| **0.5**    | **0.7901**    | **0.7028** | **0.7439**   | **0.8200**   | 🟢 **RECOMENDADO: Equilibrio óptimo** |
| 0.6    | 0.8286    | 0.5961 | 0.6934   | 0.8039   | 🟡 Mejor Precision |
| 0.7    | 0.8520    | 0.5105 | 0.6385   | 0.7850   | 🔴 Bajo Recall |

### 📂 Archivos Generados (FASE 7):
1. ✅ `config_mejor_modelo.json` — Configuración ganadora (3,677 bytes)
2. ✅ `resultados_cv.csv` — Resultados detallados de CV (10,940 bytes)
3. ✅ `analisis_umbrales.csv` — Análisis de 5 umbrales (444 bytes)
4. ✅ `roc_curve.png` — Curva ROC + Matriz de Confusión (253,797 bytes)
5. ✅ `03_notebooks/06_Modelizacion.ipynb` — Notebook completo con 10 PASOS

### ⭐ Top 10 Variables por Coeficiente (Importancia para Predicción):

| Ranking | Variable | Coeficiente | Dirección |
|---------|----------|-------------|-----------|
| 1 | tiempo_en_site_total_mms | +1.096 | ✅ Aumenta compra |
| 2 | ocupacion_Not Provided | -0.731 | ❌ Disminuye compra |
| 3 | ult_actividad_SMS Sent | +0.582 | ✅ Aumenta compra |
| 4 | ocupacion_Working Professional | +0.578 | ✅ Aumenta compra |
| 5 | fuente_Direct Traffic | -0.546 | ❌ Disminuye compra |
| 6 | origen_Lead Add Form | +0.467 | ✅ Aumenta compra |
| 7 | ult_actividad_Chat Conversation | -0.441 | ❌ Disminuye compra |
| 8 | ult_actividad_Email Bounced | -0.399 | ❌ Disminuye compra |
| 9 | fuente_Google | -0.390 | ❌ Disminuye compra |
| 10 | origen_Landing Page Submission | -0.367 | ❌ Disminuye compra |

### ⭐ Dataframe Actual (POST-PRESELECCIÓN) ✨ PARA REFERENCIAS

**Archivo:** `02_datos/03_Entrenamiento/05_train_tablon_preseleccion.pkl`

**Estructura del dataframe:**
```
<class 'pandas.DataFrame'>
Index: 6279 entries, 1242 to 1607
Data columns (total 23 columns):
 #   Column                                  Non-Null Count  Dtype  
---  ------                                  --------------  -----  
 0   compra                                  6279 non-null   int64  
 1   ambito_Not Specified                    6279 non-null   int64  
 2   ambito_Retail Management                6279 non-null   int64  
 3   ambito_Select                           6279 non-null   int64  
 4   fuente_Direct Traffic                   6279 non-null   int64  
 5   fuente_Google                           6279 non-null   int64  
 6   fuente_Organic Search                   6279 non-null   int64  
 7   fuente_Press_Release                    6279 non-null   int64  
 8   fuente_Referral Sites                   6279 non-null   int64  
 9   ocupacion_Not Provided                  6279 non-null   int64  
 10  ocupacion_Working Professional          6279 non-null   int64  
 11  origen_Landing Page Submission          6279 non-null   int64  
 12  origen_Lead Add Form                    6279 non-null   int64  
 13  paginas_vistas_visita_mms               6279 non-null   float64
 14  tiempo_en_site_total_mms                6279 non-null   float64
 15  ult_actividad_Chat Conversation         6279 non-null   int64  
 16  ult_actividad_Converted to Lead         6279 non-null   int64  
 17  ult_actividad_Email Bounced             6279 non-null   int64  
 18  ult_actividad_Had a Phone Conversation  6279 non-null   int64  
 19  ult_actividad_Page Visited on Website   6279 non-null   int64  
 20  ult_actividad_SMS Sent                  6279 non-null   int64  
 21  usuario_nuevo                           6279 non-null   int64  
 22  visitas_total_mms                       6279 non-null   float64
dtypes: float64(3), int64(20)
memory usage: 1.1 MB

```

**Resumen de preselección:**
- **Variables iniciales:** 66 features
- **Variables tras RFECV L1:** 24 features (-63.6%)
- **Variables tras desduplicación:** 24 features (sin cambios)
- **Variables finales:** 22 features (-66.7% reducción total)
- **Método:** RFECV con Regresión Logística L1
- **Reducción de multicolinealidad:** Eliminadas 2 variables altamente correlacionadas con usuario_nuevo

**Variables preseleccionadas:** Consultar `01_Documentos/Variables_preseleccionadas.txt`

**Informe detallado:** `06_resultados/Preseleccion/Informe_Preseleccion_Variables.md`

---

---

## ✨ ESTRATEGIA DE VALIDACIÓN E INTERPRETABILIDAD (CRÍTICO - OBLIGATORIO)

### 🎯 Dataset de Validación Reservado (FASE 8 - PRÓXIMA)

**Ubicación:** `C:\Users\robin\dev\01_LEADSCORING\02_datos\02_Validacion\validation.pkl`

**Propósito:** ⚠️ **Evaluación Final DEFINITIVA del modelo** (datos nunca vistos)

**Cuándo usar:** 
- ✅ SOLO DESPUÉS de completar entrenamiento definitivo del modelo
- ✅ Última evaluación con datos vírgenes
- ✅ Validación de generalización en producción

**PROHIBIDO usar para:**
- ❌ Tuning de hiperparámetros
- ❌ Cross-validation iterativa
- ❌ Selección de modelos
- ❌ Feature engineering

**Características:**
- **Registros:** 2,691 (30% del dataset original)
- **Sincronización:** Índices independientes del training set
- **Sin leakage:** ✅ Validado que NO hay IDs duplicados con training set
- **Distribución:** Balanceada con training set (37% conversión)

### 📊 Análisis de Interpretabilidad (SOLO COEFICIENTES)

**Método AUTORIZADO:** 🔴 **EXCLUSIVAMENTE coeficientes del modelo**

**Restricción CRÍTICA:** 
- ❌ **PROHIBIDO usar Permutation Importance**
- ❌ **PROHIBIDO usar SHAP o similar**
- ✅ **SOLO coeficientes directos (beta_i)**

**Implementación por Tipo de Modelo:**

| Modelo | Método de Interpretabilidad |
|--------|----------------------------|
| **Logistic Regression** ✅ | Coeficientes directos (+ ó -) |
| Modelos Lineales | Coeficientes + Intercepción |
| Random Forest | ❌ NO usar Permutation Importance |
| XGBoost | ❌ NO usar Permutation Importance |

**Para Logistic Regression (Modelo Ganador):**
- ✅ Extraer `coef_[0]` del modelo entrenado
- ✅ Magnitud = Importancia relativa
- ✅ Signo (+ ó -) = Dirección del impacto
- ✅ Visualizar Top 10 coeficientes (positivos y negativos)

**Contexto:** Enfoque simplificado en relación directa variables → predicción (sin "black box")

---

## 🎯 PRÓXIMA FASE: Scoring y Ranking Final (FASE 8)

### ✅ Prerequisitos Listos (Post-FASE 7)
- ✅ Modelo Logistic Regression entrenado (AUC=0.8898)
- ✅ Predicciones probabilísticas generadas (y_pred_proba)
- ✅ Umbral óptimo identificado (0.5 para equilibrio)
- ✅ Configuración guardada en `config_mejor_modelo.json`
- ✅ Variables aisladas sincronizadas (`id`, `no_enviar_email`)

### 📝 Próximo paso - Agente para Scoring Final
Crear notebook `07_Scoring_Final.ipynb` para:
1. Cargar predicciones del modelo (y_pred_proba con umbral 0.5)
2. Merge con variables aisladas por `id` (CRÍTICO)
3. Aplicar lógica de exclusión (no_enviar_email = 'No')
4. Ranking de leads por probabilidad de conversión (descendente)
5. Generación de reportes de leads calificados
6. Exportación en formato CSV/Excel para operaciones


## 🎯 ARCHIVOS PARA CONTINUAR CON EL PROYECTO - FASE 6 (MODELIZACIÓN)

### 📌 ARCHIVO PRINCIPAL DE TRABAJO: `05_train_tablon_preseleccion.pkl` ⭐ **NUEVO**

Este es el archivo que **DEBES USAR** para todas las operaciones de modelización desde ahora:

```
📂 02_datos/03_Entrenamiento/05_train_tablon_preseleccion.pkl
├─ Registros: 6,279
├─ Columnas: 27 (1 target + 26 features preseleccionados)
├─ Contenido:
│  ├─ compra (target): Variable binaria 0/1
│  ├─ 3 features numéricas escaladas [0,1]: visitas_total_mms, tiempo_en_site_total_mms, 
│  │  paginas_vistas_visita_mms
│  ├─ usuario_nuevo: Binaria (0=existente, 1=nuevo)
│  └─ 22 dummy variables: Codificación OneHot preseleccionada de 5 categorías
│
├─ CARACTERÍSTICAS:
│  ├─ ✅ Variables seleccionadas por RFECV L1 (máximo poder predictivo)
│  ├─ ✅ Multicolinealidad controlada (umbral correlación > 0.9)
│  ├─ ✅ Sin valores faltantes (0 nulos)
│  └─ ✅ Listo para modelización sin balanceo
│
├─ SIN (¡IMPORTANTE!):
│  ├─ ❌ id (separado en df_variables_aisladas)
│  └─ ❌ no_enviar_email (separado en df_variables_aisladas)
│
└─ USO: Train/test split → Modelización → Predicciones (SIN BALANCEO)
```

### 📌 ARCHIVO DE VARIABLES AISLADAS: `04_train_variables_aisladas.pkl`

Este archivo almacena las 2 variables que se **AISLÓ INTENCIONALMENTE** porque no entran en modelización:

```
📂 02_datos/03_Entrenamiento/04_train_variables_aisladas.pkl
├─ Registros: 6,279 (SINCRONIZADAS CON df_modelizacion)
├─ Columnas: 2
├─ Contenido:
│  ├─ id (int64): CLAVE PRIMARIA - Identificador único del lead
│  │  └─ Uso: Para realizar merge posterior con predicciones
│  │
│  └─ no_enviar_email (str "Yes"/"No"): VARIABLE DE EXCLUSIÓN POST-MODELO
│     └─ Uso: Filtrar contactos que NO deben recibir emails después del scoring
│
└─ CRÍTICO: Se mantiene INTACTA durante toda la modelización
```

---

### 🔄 LÓGICA DEL FLUJO POST-SCORING (FASE 6+) - SIN BALANCEO

**Paso 1: Durante Modelización (Fase 6 - Agente A_06_Modelizador)**
```python
# 1. Cargar el dataframe PRESELECCIONADO (sin balanceo)
df_modelo = pd.read_pickle('02_datos/03_Entrenamiento/05_train_tablon_preseleccion.pkl')

# 2. Extraer target y features
y = df_modelo['compra']
X = df_modelo.drop('compra', axis=1)

# 3. Realizar train/test split SIN BALANCEO (mantener distribución natural: 37/63)
indices_train, indices_test = train_test_split(range(len(df_modelo)), test_size=0.3, random_state=42)
X_train = X.iloc[indices_train]
X_test = X.iloc[indices_test]
y_train = y.iloc[indices_train]
y_test = y.iloc[indices_test]

# df_variables_aisladas se mantiene SEPARADA y SINCRONIZADA
df_cualif = pd.read_pickle('02_datos/03_Entrenamiento/04_train_variables_aisladas.pkl')
df_cualif_train = df_cualif.iloc[indices_train]
df_cualif_test = df_cualif.iloc[indices_test]

# 4. Entrenar modelo(s) con X_train, y_train (sin balanceo)
# 5. Realizar predicciones con X_test
y_pred_proba = modelo.predict_proba(X_test)[:, 1]
y_pred = modelo.predict(X_test)
```

**Paso 2: Después del Scoring (UNIÓN FINAL)**
```python
# 5. Crear dataframe de resultados
df_predicciones = pd.DataFrame({
    'prediction_score': y_pred,
    'prediction_label': (y_pred > 0.5).astype(int)
})

# 6. ⭐ UNIR AMBOS DATAFRAMES POR ID (¡NUNCA por índice!)
df_final = df_predicciones.merge(df_cualif_test, on='id', how='left')

# Ahora df_final contiene:
#  - prediction_score (score de conversión 0-1)
#  - prediction_label (0 o 1)
#  - id (para trazabilidad)
#  - no_enviar_email (para filtrar contactos)

# 7. LÓGICA DE NEGOCIO FINAL (POST-SCORING):
#  Aplicar reglas de exclusión según no_enviar_email
df_contactos_validos = df_final[df_final['no_enviar_email'] == 'No']

# 8. RANKING DE LEADS (leads con mayor probabilidad de compra)
df_ranking = df_contactos_validos.sort_values('prediction_score', ascending=False)

# 9. EXPORTAR para operaciones de marketing/ventas
df_ranking.to_csv('06_resultados/leads_scored_ranked.csv', index=False)
```

---

### ⚠️ RESUMEN: QUÉ HACER EN CADA FASE

| Fase | Archivo Principal | Archivo Secundario | Operación | Balanceo |
|------|-------------------|-------------------|-----------|----------|
| **5 (✅)** Preselección | `04_train_tablon_transformado.pkl` | - | RFECV L1, desduplicación | N/A |
| **6 (⏭️)** Modelización | `05_train_tablon_preseleccion.pkl` ⭐ | `04_train_variables_aisladas.pkl` (SINCRONIZADO) | Train/test split, ajustar modelo | ⊘ **SIN BALANCEO** |
| **7** Evaluación | Predicciones del modelo | `04_train_variables_aisladas.pkl` | Merge por `id` | N/A |
| **8** Scoring Final | `df_predicciones` + `df_cualificacion` | Reglas de negocio | Filtrar, rankear, exportar | N/A |

---

## 🔐 REGLAS DE INTEGRIDAD DE DATOS - OBLIGATORIAS

### ⚠️ REGLA 1: Merge SIEMPRE por `id`
```python
# ✅ CORRECTO
df_final = df_predicciones.merge(df_cualificacion, on='id', how='left')

# ❌ PROHIBIDO: Merge por índice
df_final = pd.concat([df_predicciones, df_cualificacion], axis=1)
```

### ⚠️ REGLA 2: Sincronizar Ambos Dataframes en Train/Test Split
```python
# ❌ PROHIBIDO
X_train, X_test = train_test_split(df_modelizacion)  # ← df_cualificacion queda desalineado

# ✅ CORRECTO: Usar MISMOS índices en AMBOS
indices_train, indices_test = train_test_split(range(len(df_modelizacion)))
X_train = df_modelizacion.iloc[indices_train]
X_test = df_modelizacion.iloc[indices_test]
df_cualif_train = df_cualificacion.iloc[indices_train]  # ← CRÍTICO
df_cualif_test = df_cualificacion.iloc[indices_test]    # ← CRÍTICO

# Validación
assert (X_train['id'].values == df_cualif_train['id'].values).all()
```

### ⚠️ REGLA 3: Validación Post-Operación
```python
# Después de cualquier operación que afecte orden:
assert len(df_modelizacion) == len(df_cualificacion), "❌ ERROR: Tamaños diferentes"
df_merged = df_modelizacion.merge(df_cualificacion, on='id', how='inner')
assert len(df_merged) == 6279, "❌ ERROR: Pérdida de registros en merge"
```

### 🚫 Errores Comunes Prohibidos

| Error | Impacto | Solución |
|-------|--------|----------|
| `pd.concat([df_m, df_c], axis=1)` | Misalignment silencioso | `.merge(on='id')` |
| `train_test_split(df_modelo)` solo | df_cualif desalineado | Split ambos con MISMO índice |
| `df.reset_index(drop=True)` sin actualizar | Desalineación fatal | Reset ambos simultáneamente |
| `df.drop_duplicates()` en uno | Registros fantasma | Aplicar a AMBOS |

---

### 🔍 Dataframe Anterior (POST-EDA)
**Archivo:** `02_datos/03_Entrenamiento/03_train_tablon_eda.pkl` (referencia histórica)
```
Registros:      6,279
Columnas:       21 (sin transformaciones)
Nulos totales:  0
Tamaño:         1.52 MB
Transformaciones: NINGUNA (análisis exploratorio solo)
```

### 🔧 Transformaciones Aplicadas por Agente A_02:
- ✅ P1: Imputados 16 nulos en `fuente` con "Unknown"
- ✅ P2: Imputados 1,017 nulos en `ambito` con "Not Specified"
- ✅ P3: Imputados 1,908 nulos en `ocupacion` con "Not Provided"
- ✅ P4: Validados valores en `visitas_total` (no hay negativos)
- ✅ P5: Eliminadas `conociste_revista`, `conociste_youtube` (sin varianza)
- ✅ P6: Eliminada `no_llamar` (99.98% un solo valor)

### Datasets Originales - TRAIN/VALIDATION SPLIT

#### Dataset de Entrenamiento (TRAIN - Original)
- **Archivo:** `02_datos/03_Entrenamiento/01_train_tablon_integrado.pkl`
- **Registros:** 6,279 (70.0%)
- **Tamaño:** 1.67 MB
- **Conversión:** 37.19% (2,335 compras)
- **Balance usuario_nuevo:** 45.74% nuevos, 54.26% existentes

#### Dataset de Validación (VALIDATION)
- **Archivo:** `02_datos/02_Validacion/validation.pkl`
- **Registros:** 2,691 (30.0%)
- **Tamaño:** 0.72 MB
- **Conversión:** 37.05% (998 compras)
- **Balance usuario_nuevo:** 45.75% nuevos, 54.25% existentes

#### Validación de Leakage
- ✅ IDs únicos en TRAIN: 6,279
- ✅ IDs únicos en VALIDATION: 2,691
- ✅ IDs comunes (leakage): 0 → **SIN LEAKAGE**

#### Estructura del Dataframe Final

```python
Información general:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 8970 entries, 0 to 8969
Columns: 24 entries

Variables numéricas (10):
  - id (int64) - Clave primaria
  - compra (int64) - Target (0/1)
  - visitas_total (float64) - Limpio desde FASE 1
  - tiempo_en_site_total (int64)
  - paginas_vistas_visita (float64) - Limpio desde FASE 1
  - score_actividad (float64) - Imputado en FASE 2
  - score_perfil (float64) - Imputado en FASE 2
  - tiene_score_actividad (int64)
  - tiene_score_perfil (int64)
  - usuario_nuevo (int64) - Creado en FASE 2

Variables categóricas (14):
  - origen (object) - Cómo llegó el lead
  - fuente (object) - Canal de tráfico
  - no_enviar_email (object) - Preferencia
  - no_llamar (object) - Preferencia
  - ult_actividad (object) - Última acción
  - ambito (object) - Ámbito profesional
  - ocupacion (object) - Ocupación
  - conociste_google (object)
  - conociste_revista (object)
  - conociste_periodico (object)
  - conociste_youtube (object)
  - conociste_facebook (object)
  - conociste_referencias (object)
  - descarga_lm (object) - Descargó lead magnet
```

---

## 📁 ESTRUCTURA DE CARPETAS

```
01_LEADSCORING/
├── 03_notebooks/
│   ├── 01_Importacion_Datos.ipynb      ← Importación + Limpieza + Imputación (FASES 1-5)
│   └── 02_Calidad_Datos.ipynb          ← Enfocado en Calidad: FASE 1 + FASE 2
├── 02_datos/
│   ├── 01_Originales/
│   │   └── Leads.csv                   (Fuente original - 9,093 registros)
│   ├── 02_Validacion/
│   │   └── validation.pkl              ✨ NUEVA (FASE 4) - 2,691 registros (30%)
│   └── 03_Entrenamiento/
│       ├── df_leads_clean.csv          (v1 - Original)
│       ├── df_leads_clean_v2.csv       (v2 - Post-limpieza)
│       ├── df_leads_clean_v3.csv       (v3 - Final limpio)
│       └── 01_train_tablon_integrado.pkl   ✨ NUEVA (FASE 4) - 6,279 registros (70%)
├── 06_resultados/
│   ├── eda_summary.json
│   ├── limpieza_log.json
│   ├── imputacion_log.json
│   └── ...
├── INFORME_CALIDAD_DATOS.md            (Documentación Fase 2)
├── copilot-instructions.md             (Este archivo)
└── README.md
```

---

## 🎯 RESUMEN DE NOTEBOOKS DISPONIBLES

### `03_notebooks/02_Calidad_Datos.ipynb` ⭐ RECOMENDADO
**Propósito:** Análisis y validación de calidad de datos  
**Contenido:**
- 18 celdas organizadas en FASE 1 + FASE 2
- Importación de v1 y transformaciones paso a paso
- Validaciones detalladas post-limpieza e imputación
- Estadísticas de scores por grupo (usuario_nuevo)
- Tasas de conversión por segmento
- Outputs: df_leads_clean_v2.csv, df_leads_clean_v3.csv

**Cuándo usarlo:** Para entender, validar o documentar la calidad de datos

### `03_notebooks/01_Importacion_Datos.ipynb`
**Propósito:** Flujo completo de procesamiento (documentación histórica)  
**Contenido:**
- Importación + FASE 1 + FASE 2 + análisis detallado
- Comparativas entre versiones (v1, v2, v3)
- Archivos JSON generados (eda_summary, limpieza_log, imputacion_log)
- Información general del dataset final

**Cuándo usarlo:** Para referencia histórica o documentación completa

---

## 💻 CÓMO CONTINUAR CON FASE 5 (MODELIZACIÓN) - PRÓXIMO PASO ⭐

### ✅ Prerequisitos Listos
- ✅ `04_train_tablon_transformado.pkl` generado (6,279 × 67)
- ✅ `04_train_variables_aisladas.pkl` generado (6,279 × 2)
- ✅ Transformaciones completadas (MinMaxScaler + OneHot)
- ✅ Variables aisladas separadas (id + no_enviar_email)

### 📝 Crear Notebook `05_Modelizacion.ipynb`

```python
# 1. CARGAR AMBOS DATAFRAMES
import pandas as pd
from sklearn.model_selection import train_test_split

df_modelo = pd.read_pickle('02_datos/03_Entrenamiento/04_train_tablon_transformado.pkl')
df_cualif = pd.read_pickle('02_datos/03_Entrenamiento/04_train_variables_aisladas.pkl')

# 2. EXTRAER TARGET Y FEATURES
y = df_modelo['compra']
X = df_modelo.drop('compra', axis=1)

# 3. ⭐ TRAIN/TEST SPLIT SINCRONIZADO (¡AMBOS DATAFRAMES!)
indices = range(len(df_modelo))
idx_train, idx_test = train_test_split(indices, test_size=0.3, random_state=42)

X_train = X.iloc[idx_train]
X_test = X.iloc[idx_test]
y_train = y.iloc[idx_train]
y_test = y.iloc[idx_test]

# ⭐ SINCRONIZAR df_cualificacion con MISMO índice
df_cualif_train = df_cualif.iloc[idx_train]
df_cualif_test = df_cualif.iloc[idx_test]

# 4. VALIDACIÓN CRÍTICA
assert len(X_train) == len(df_cualif_train), "❌ ERROR: Tamaños diferentes en train"
assert len(X_test) == len(df_cualif_test), "❌ ERROR: Tamaños diferentes en test"
print("✅ Sincronización correcta entre X y df_cualificacion")

# 5. ENTRENAR MODELO(S)
from sklearn.linear_model import LogisticRegression
modelo = LogisticRegression(random_state=42)
modelo.fit(X_train, y_train)

# 6. PREDICCIONES
y_pred_proba = modelo.predict_proba(X_test)[:, 1]
y_pred = modelo.predict(X_test)

# 7. EVALUACIÓN
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")

# 8. GUARDAR PREDICCIONES + variables aisladas
df_resultados = pd.DataFrame({
    'prediction_proba': y_pred_proba,
    'prediction': y_pred
})

# ⭐ MERGE POR ID (crucial para post-scoring)
df_final = df_resultados.merge(df_cualif_test[['id', 'no_enviar_email']], 
                                 left_index=True, right_index=True, how='left')

# 9. APLICAR LÓGICA DE NEGOCIO
df_validos = df_final[df_final['no_enviar_email'] == 'No']
df_ranking = df_validos.sort_values('prediction_proba', ascending=False)

print(f"Leads para contactar: {len(df_ranking)}")
print(f"Leads excluidos (no_enviar_email): {len(df_final) - len(df_ranking)}")
```

### 🎯 Checklist para Fase 5
- [ ] Crear notebook `05_Modelizacion.ipynb`
- [ ] Cargar ambos dataframes (`04_train_tablon_transformado.pkl` + `04_train_variables_aisladas.pkl`)
- [ ] Implementar train/test split **sincronizado en AMBOS**
- [ ] Validar que sincronización es correcta (asserts)
- [ ] Entrenar modelos (Logistic Regression, Random Forest, etc.)
- [ ] Evaluar con métricas apropiadas (ROC-AUC, precision, recall)
- [ ] Generar predicciones y hacer merge por `id` con df_cualificacion
- [ ] Aplicar lógica de exclusión (no_enviar_email = "No")
- [ ] Rankear leads por probabilidad de conversión
- [ ] Guardar resultados finales en `06_resultados/`

---

## 💻 CÓMO CONTINUAR

### Notebooks Disponibles

**`03_notebooks/01_Importacion_Datos.ipynb`**
- Contiene: Carga de datos + FASE 1 (limpieza) + FASE 2 (imputación)
- Uso: Referencia completa del flujo end-to-end
- Salida: df_leads_clean_v2.csv y df_leads_clean_v3.csv

**`03_notebooks/02_Calidad_Datos.ipynb`** ⭐ (Recomendado para análisis de calidad)
- Contiene: Solo FASE 1 + FASE 2 con análisis detallado
- Uso: Enfocado en validación y estadísticas de calidad
- Salida: Resumen de transformaciones y validaciones

### Para la Próxima Sesión (Fase 3: EDA Actualizado)

1. **Cargar Dataset v3**
   ```python
   df = pd.read_csv('02_datos/03_Entrenamiento/df_leads_clean_v3.csv', sep=';')
   ```

2. **Análisis por Segmento**
   - Comparar distribuciones usuario_nuevo=0 vs usuario_nuevo=1
   - Calcular poder predictivo de cada variable
   - Identificar variables más relevantes

3. **Visualizaciones Recomendadas**
   - Distribuciones univariantes por grupo
   - Correlaciones con target (compra)
   - Boxplots de numéricas por target
   - Gráficos de barras para categóricas
   - Crear notebook `03_EDA_Actualizado.ipynb` en `03_notebooks/`

### Decisiones Documentadas para No Rehacer

- ✅ Eliminación de 123 registros: Justificada por datos críticos faltantes
- ✅ Imputación con ceros: Coherente con usuarios nuevos sin historial
- ✅ Variable usuario_nuevo: Captura segmentación importante
- ✅ Dataset v3: Usar ESTE, no v1 o v2

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### NO HACER
- ❌ Usar df_leads_clean.csv (v1) - tiene nulos
- ❌ Usar df_leads_clean_v2.csv para scoring - le faltan variables
- ❌ Eliminar o modificar variable usuario_nuevo - es clave para segmentación
- ❌ Re-imputar scores - ya está hecho en v3

### SÍ HACER
- ✅ Usar df_leads_clean_v3.csv exclusivamente
- ✅ Respetar la segmentación usuario_nuevo en análisis
- ✅ Documentar cualquier transformación adicional
- ✅ Referirse a INFORME_CALIDAD_DATOS.md para contexto

---

## 📋 COLUMNAS QUE REQUIEREN PROCESAMIENTO EN SIGUIENTE FASE

### Variables Numéricas a Transformar
```
tiempo_en_site_total:       Considerar log() - probablemente sesgada
visitas_total:              Considerar binning o log()
paginas_vistas_visita:      Revisar outliers
```

### Variables Categóricas a Dummificar
```
origen, fuente, ult_actividad, ambito, ocupacion
conociste_google, conociste_revista, ...
descarga_lm, no_enviar_email, no_llamar
```

### Escalado Necesario
- Normalizar numéricas si usaremos modelos sensibles a escala (KNN, SVM)
- No necesario para árboles (Decision Trees, Random Forest)

---

## 📚 REFERENCIAS Y DOCUMENTACIÓN

### Notebooks
- **`03_notebooks/01_Importacion_Datos.ipynb`** - Flujo completo (importación + limpieza + imputación)
- **`03_notebooks/02_Calidad_Datos.ipynb`** - Enfocado en calidad de datos (FASE 1 + FASE 2)

### Documentación
- **INFORME_CALIDAD_DATOS.md** - Resumen ejecutivo de Fase 2
- **copilot-instructions.md** - Este archivo (guía del proyecto)

### JSON Logs
- `06_resultados/eda_summary.json` - Resumen de análisis exploratorio
- `06_resultados/limpieza_log.json` - Detalles de eliminación de nulos
- `06_resultados/imputacion_log.json` - Detalles de imputación de scores

---

## 🎓 NOTAS METODOLÓGICAS

### Estrategia de Imputación Documentada

**Pregunta:** ¿Por qué imputar con cero en lugar de media/mediana?

**Respuesta:** 
- Los nulos en usuarios nuevos son No-Missing-At-Random (NMAR)
- El valor cero es semánticamente correcto: "sin historial"
- Imputar con media/mediana hubiera ocultado la distinción usuario_nuevo
- La variable usuario_nuevo captura el efecto de la imputación

### Hipótesis de Modelado
- Usuario_nuevo puede tener comportamiento diferente
- Scores de actividad/perfil son predictores fuertes para usuarios existentes
- La ausencia de datos en usuarios nuevos es información valiosa

---

## 🔐 CHANGELOG

### 2026-06-09 (v2.1) - FASE 7 MODELIZACIÓN COMPLETA Y CONSOLIDADA ✨ ACTUALIZACIÓN FINAL
- ✅ **FASE 7: MODELIZACIÓN COMPLETADA CON CONSOLIDACIÓN EN NOTEBOOK ÚNICO**
  - **Método:** Validación Cruzada 5-Fold Estratificado + Entrenamiento en Todo el Dataset
  - **Modelo Ganador:** Logistic Regression (L2 regularization)
  - **Hiperparámetros Óptimos:** C=100.0, solver='lbfgs', max_iter=1000, tol=0.0001
  - **Métrica Principal: AUC-ROC = 0.8898** ⭐ (Dataset completo)
    - CV AUC mean: 0.8864 ± 0.0031 (5-fold)
    - Accuracy: 82.00% | Precision: 79.01% | Recall: 70.28% | F1: 0.7439
    - Overfitting: Mínimo (diferencia 0.0034)
  - **Análisis de Umbrales:** Recomendado umbral=0.5 para equilibrio Precision-Recall
  - **Interpretabilidad:** Top 10 coeficientes identificados:
    - 🔝 Variable más predictiva: tiempo_en_site_total_mms (+1.096)
    - Coeficientes para dirección de impacto (positivo/negativo) documentados
- ✅ **Estructura del Notebook: 10 PASOS Completados**
  - PASO 1: Carga del dataset preseleccionado (6,279 × 27)
  - PASO 2: Preparación de features (escalado StandardScaler)
  - PASO 3: Configuración de StratifiedKFold(5)
  - PASO 4: Búsqueda de hiperparámetros (RandomizedSearchCV, 30 iteraciones)
  - PASO 5: Evaluación en validación cruzada (5 métricas)
  - PASO 6: Análisis de importancia (coeficientes + Permutation Importance)
  - PASO 7: Entrenamiento final en todo el dataset
  - PASO 8: Cálculo de AUC y métricas detalladas
  - PASO 9: Curva ROC y visualizaciones (PNG guardado)
  - PASO 10: Análisis de umbrales de decisión (5 puntos evaluados)
- ✅ **Archivos Generados en 06_resultados/Modelizacion/:**
  - `config_mejor_modelo.json` (3.7 KB) — Configuración completa para reproducibilidad
  - `resultados_cv.csv` (10.9 KB) — Detalles de todas las iteraciones de RandomizedSearchCV
  - `analisis_umbrales.csv` (444 B) — Métricas para 5 umbrales diferentes
  - `roc_curve.png` (254 KB, 300 DPI) — Curva ROC + Matriz de Confusión
- ✅ **Validación y Calidad:**
  - ✅ Todos los PASOS ejecutados sin errores
  - ✅ Variables sincronizadas correctamente
  - ✅ Métricas CV vs Entrenamiento consistentes
  - ✅ Visualizaciones profesionales generadas
- ✅ **Próxima Fase:** FASE 8 - Scoring Final y Ranking de Leads
- ✅ **Restricciones Documentadas:**
  - ⊘ SIN balanceo (37% conversión natural preservada)
  - ✅ Coeficientes + Permutation Importance para interpretabilidad
  - ✅ StandardScaler aplicado pre-training

### 2026-06-05 (v2.0) - FASE 6 MODELIZACIÓN COMPLETADA ✨ MAJOR RELEASE
- ✅ **FASE 6: MODELIZACIÓN COMPLETADA - SUBAGENT-DRIVEN DEVELOPMENT**
  - Método: Validación Cruzada 5-Fold Estratificado + Validation Set
  - **Logistic Regression seleccionado:** ROC-AUC = 0.8848 (Supera objetivo 0.80 ✅)
    - CV AUC mean: 0.8862 ± 0.0075
    - Validation AUC: 0.8848 (Overfitting mínimo: 0.0016 diferencia)
    - Precision: 0.8481, Recall: 0.8013, F1: 0.8241, Accuracy: 0.8434
  - XGBoost referencia: ROC-AUC = 0.8685
  - Interpretabilidad: Top 10 features positivos y negativos (coeficientes)
  - 12 tasks completadas por subagents: Notebook base → CV → LR + XGBoost → Evaluación → Análisis → Visualizaciones → Reporte
- ✅ **Artefactos generados:**
  - Notebook ejecutable: `03_notebooks/06_Modelizacion.ipynb` (13 celdas, código production-ready)
  - Modelos entrenados: Logistic Regression + XGBoost (pickle format)
  - Resultados CV + Validation: JSON con métricas 5-fold
  - Reporte profesional: `Reporte_Modelizacion.md` (6,393 bytes)
  - Visualizaciones: ROC curves, confusion matrices, top 15 coefficients (PNG 300dpi)
  - Documentación: Design spec + Implementation plan guardados
- ✅ **Próximo paso:** FASE 7 - Scoring y Ranking Final
- ✅ **Restricciones aplicadas:** 
  - NO balanceo de clases (37% conversión natural preservada)
  - NO permutation importance (solo coeficientes)
  - validation.pkl reservado solo para prueba final

### 2026-06-05 (v1.9) - VALIDACIÓN E INTERPRETABILIDAD DOCUMENTADAS
- ✅ **Estrategia de Validación Final:**
  - Dataset reservado: `02_datos/02_Validacion/validation.pkl` (2,691 registros)
  - Propósito: Verificación final post-entrenamiento definitivo
  - Restricción: NO usar para tuning, solo para evaluación final
  - Sin leakage validado con training set
- ✅ **Estrategia de Interpretabilidad:**
  - Método autorizado: SOLO coeficientes del modelo
  - Restricción: ❌ NO usar permutation importance
  - Aplicable a: Regresión Logística (coeficientes), modelos lineales
  - Documentación: Nueva sección "ESTRATEGIA DE VALIDACIÓN E INTERPRETABILIDAD"
- ✅ **copilot-instructions.md ACTUALIZADO:**
  - Agregada sección crítica antes de Modelización
  - Detalles de cuándo/cómo usar validation.pkl
  - Especificación exacta de método de interpretabilidad

### 2026-06-05 (v1.8) - PRESELECCIÓN DE VARIABLES COMPLETADA + DECISIÓN SIN BALANCEO ✨ NUEVO
- ✅ **Agente A_05_SeleccionadorVariables: Preselección de Variables**
  - MÉTODO PRINCIPAL: RFECV con Regresión Logística L1 ✅
  - REDUCCIÓN: 66 features → 26 features (-60.6% reducción)
  - DESDUPLICACIÓN INTELIGENTE ✅
    - Análisis de correlaciones (umbral > 0.9)
    - Identificación de variables correlacionadas con usuario_nuevo
    - Eliminación de 2 variables redundantes
  - ARCHIVOS GENERADOS ✅
    - `02_datos/03_Entrenamiento/05_train_tablon_preseleccion.pkl` (6,279 × 27)
    - `01_Documentos/Variables_preseleccionadas.txt` (lista de 26 variables)
    - `03_notebooks/05_Preseleccion_Variables.ipynb` (notebook ejecutado)
- ✅ **DECISIÓN CRÍTICA: SIN BALANCEO DE CLASES**
  - Distribución natural mantenida: 37% conversión (2,335 casos positivos)
  - Razón: Representa fielmente el caso de uso en producción
  - FASE 6 (Balanceo) SALTADA
  - Próxima fase: A_06_Modelizador (FASE 6, no FASE 7)
- ✅ **INSTRUCCIÓN PARA MODELIZADOR:**
  - Archivo principal: `05_train_tablon_preseleccion.pkl` (26 features preseleccionados)
  - Train/test split: SIN balanceo (ratio natural 70/30)
  - Modelos recomendados: Logistic Regression, Random Forest, XGBoost
  - Mantener df_variables_aisladas sincronizado en splits
- ✅ **copilot-instructions.md ACTUALIZADO:**
  - Sección PRÓXIMAS FASES: Fase 5 ✅, Fase 6 ⊘ saltada, Fase 6 ⏭️ Modelización
  - Sección ARCHIVOS: Cambio de 04_train_tablon_transformado.pkl → 05_train_tablon_preseleccion.pkl
  - Tabla de fases: Agregada columna "Balanceo" con indicación ⊘ SIN BALANCEO
  - Código ejemplo: Actualizado para preselección sin balanceo

### 2026-06-05 (v1.7) - PREPARACIÓN DE DATOS ACTUALIZADA + ESTRATEGIA DE DOS DATAFRAMES ✨ ACTUALIZADO
- ✅ **Agente A_04_PreparadorDatos: Transformaciones Finales para Modelización**
  - FASE 1: Transformaciones numéricas ✅ (5 con MinMaxScaler [0,1], 1 sin transformar)
  - FASE 2: OneHotEncoding ✅ (6 categóricas → 60 dummies, drop='first')
  - FASE 3: Variables aisladas ✅ (id + no_enviar_email separadas)
  - FASE 4: Unión y validaciones ✅ (7 validaciones críticas pasadas)
  - FASE 5: Guardado ✅ (2 pickles + metadatos JSON)
  - FASE 6: Documentación de merge seguro ✅
- ✅ **Arquitectura Final (DOS DATAFRAMES):**
  - **DF Modelización:** `02_datos/03_Entrenamiento/04_train_tablon_transformado.pkl` (6,279 × 67)
    - Contenido: compra + 5 numéricas (MinMax) + 60 dummies + usuario_nuevo
    - Sin: id, no_enviar_email
    - Uso: Modelización, train/test split, predicciones
  - **DF Cualificación:** `02_datos/03_Entrenamiento/04_train_variables_aisladas.pkl` (6,279 × 2)
    - Contenido: id (CLAVE DE UNIÓN), no_enviar_email
    - Uso: Merge post-modelo para filtrar/excluir contactos
- ✅ **Transformaciones Aplicadas:**
  - MinMaxScaler [0,1]: visitas_total, tiempo_en_site_total, paginas_vistas_visita, score_actividad, score_perfil
  - Sin transformación: usuario_nuevo (formato correcto)
  - OneHotEncoder (drop='first'): origen (3), fuente (16), ult_actividad (15), ambito (19), ocupacion (6), descarga_lm (1) = **60 dummies**
- ✅ **Validaciones Críticas:**
  - ✅ 6,279 filas preservadas
  - ✅ Target 'compra' binario (0/1)
  - ✅ 0 valores NaN
  - ✅ 67 columnas únicas
  - ✅ Target en primera posición
  - ✅ Variables aisladas intactas
- ✅ **Reglas de Integridad Documentadas:**
  - REGLA 1: Merge SIEMPRE por `id`, NUNCA por índice
  - REGLA 2: Train/test split sincronizado en AMBOS dataframes
  - REGLA 3: Validación post-operación obligatoria
- ✅ **Documentación Generada:**
  - `01_Documentos/PlantillaTransformaciones.xlsx` (matriz de diseño)
  - `02_datos/03_Entrenamiento/04_train_metadata_transformacion.json` (metadatos)
  - `.github/copilot-instructions.md` actualizado con estrategia de 2 dataframes
  - Sección "REGLAS DE INTEGRIDAD DE DATOS" añadida
- 🎯 **Próximo agente:** A_05_Modelizacion (usar DF de modelización, mantener DF de cualificación sincronizado en splits)

### 2026-06-04 (v1.5) - EDA COMPLETADO CON ANÁLISIS AVANZADO ✨ ACTUALIZADO
- ✅ **Análisis Exploratorio Completo (7 Tareas)**
  - TAREA 1: Carga y tipificación ✅ (6 discretas, 4 continuas, 5 categóricas, 2 booleanas)
  - TAREA 2: Estadísticas numéricas ✅ (percentiles, skewness, kurtosis, outliers IQR)
  - TAREA 3: Gráficos numéricas ✅ (KDE, boxplots, correlación con target)
  - TAREA 4: Estadísticas categóricas ✅ (frecuencias, tasas conversión, raros, Cramér's V)
  - TAREA 5: Gráficos categóricas ✅ (barras, heatmaps de interacción)
  - TAREA 6: Análisis alta cardinalidad ✅ (umbral 15+ categorías, índice Herfindahl)
  - TAREA 7: Análisis texto y fecha ✅ (verificación de tipos especiales)
- ✅ **Transformaciones Aplicadas en EDA:**
  - Agrupamiento `fuente`: Categorías <5% → "Otros" (5 → 5 categorías)
  - Agrupamiento `ult_actividad`: Categorías <3% → "Otros" (16 → 8 categorías)
- ✅ **Hallazgos Principales:**
  - Mejor predictor: tiempo_en_site_total (r=0.378)
  - Alta concentración: origen (54% Landing Page), ocupacion (59% Unemployed)
  - Variables sin varianza detectadas en fase anterior (eliminadas)
  - Distribuciones sesgadas: visitas_total (skewness=21.99), paginas_vistas (skewness=3.39)
- ✅ **Documentación Completa:**
  - 27+ gráficos profesionales en 06_resultados/EDA_graficos/
  - Clasificación de variables: 06_resultados/clasificacion_variables.json
  - Análisis de alta cardinalidad: Dentro del notebook con índice Herfindahl
- ✅ **Estado Final:**
  - Sin variables de texto detectadas (todas categóricas con cardinalidad manejable)
  - Sin variables de fecha (dataset enfocado en comportamiento actual)
  - 6,279 registros × 17 columnas (post-limpieza)

### 2026-06-02 (v1.3) - AGENTE A_02 COMPLETADO
- ✅ **Análisis Exhaustivo de Calidad (9 Tareas obligatorias)**
  - TAREA 1: Nombres normalizados ✅ (0 cambios necesarios)
  - TAREA 2: Tipos de datos validados ✅
  - TAREA 3: 0 duplicados completos ✅
  - TAREA 4-9: Análisis univariantes, outliers, reglas lógicas ✅
- ✅ **6 Propuestas de Corrección APLICADAS:**
  - P1: 16 nulos en `fuente` → "Unknown"
  - P2: 1,017 nulos en `ambito` → "Not Specified"
  - P3: 1,908 nulos en `ocupacion` → "Not Provided"
  - P4: Validación de `visitas_total` (1,439 = 0 son válidos)
  - P5-P6: Eliminadas 3 columnas sin varianza
- ✅ **Dataframe Limpio Generado:**
  - `02_datos/03_Entrenamiento/02_train_tablon_calidad.pkl` (1.52 MB)
  - `02_datos/03_Entrenamiento/df_leads_clean_calidad.csv` (0.75 MB)
  - 6,279 registros × 21 columnas (0 nulos)

### 2026-06-02 (v1.2) - FASE 4 COMPLETADA
- ✅ **FASE 4: Separación Train/Validation SIN LEAKAGE**
- ✅ Split 70/30 estratificado (6,279 train / 2,691 validation)
- ✅ Validado: NO hay IDs duplicados entre train y validation
- ✅ Balance preservado en ambos datasets (37% conversión)
- ✅ Archivos generados:
  - `02_datos/03_Entrenamiento/01_train_tablon_integrado.pkl`
  - `02_datos/02_Validacion/validation.pkl`
- ✅ Documentado en copilot-instructions.md

### 2026-06-02 (v1.1) - Actualización de Notebooks
- ✅ Creado `03_notebooks/02_Calidad_Datos.ipynb` (enfocado en calidad)
- ✅ Actualizado `03_notebooks/01_Importacion_Datos.ipynb` (flujo completo)
- ✅ Reorganizada estructura: notebooks en carpeta `03_notebooks/`
- ✅ Actualizado copilot-instructions.md con nueva estructura
- ✅ Dataset v3 validado en ambos notebooks

### 2026-06-02 (v1.0) - Creación Inicial
- ✅ Creado copilot-instructions.md v1.0
- ✅ Completada Fase 2 de calidad de datos
- ✅ Documentado en INFORME_CALIDAD_DATOS.md
- ✅ Dataset v3 generado y validado

---

**Próxima revisión:** Después de Fase 8 (Scoring y Ranking Final)  
**Responsable:** Agente para Scoring (A_08_Scorer)  
**Estado actual:** ✅ FASE 7 (MODELIZACIÓN) COMPLETADA - Logistic Regression (AUC=0.8898)
