# Auditoría de Integración y Limpieza - A_08_Limpieza

**Fecha:** 2026-06-09  
**Generado por:** Agente A_08_PreProduccionLimpieza  
**Versión:** 1.0

---

## FASE 0 — MAPEO DEL PROYECTO (Completada)

### Estructura del Proyecto
- **Directorio raíz:** `C:\Users\robin\dev\01_LEADSCORING`
- **Carpetas validadas:**
  - ✅ `02_datos/01_Originales/` - Datos originales
  - ✅ `02_datos/02_Validacion/` - Validation set (reservado para FASE 8)
  - ✅ `02_datos/03_Entrenamiento/` - Datasets de entrenamiento
  - ✅ `03_notebooks/` - Notebooks de análisis y modelización
  - ✅ `06_resultados/` - Resultados de análisis
  - ✅ `07_despliegue/pre-produccion/` - Artefactos de pre-producción

### CSV Original Identificado
- **Archivo:** `Leads.csv`
- **Ubicación:** `02_datos/01_Originales/Leads.csv`
- **Registros originales:** 9,093
- **Columnas originales:** 23
- **Clave primaria:** `id` (valores únicos: 9,093)

### Notebooks de Desarrollo Identificados
| Archivo | Agente | Descrip ción |
|---------|--------|-------------|
| `01_Importacion_Datos.ipynb` | A_01 | Carga CSV, limpieza básica, split train/val |
| `02_Calidad_Datos.ipynb` | A_02 | Análisis exhaustivo de calidad, correcciones |
| `03_EDA.ipynb` | A_03 | Análisis exploratorio (NO transformaciones) |
| `04_Preparacion_Datos.ipynb` | A_04 | MinMaxScaler, OneHotEncoding, preparación |
| `05_Preseleccion_Variables.ipynb` | A_05 | Selección de features (mutual_info_classif) |
| `06_Modelizacion.ipynb` | A_07 | Logistic Regression, RandomizedSearchCV, AUC 0.8898 |

---

## FASE 1 — INTEGRACIÓN LINEAL (Completada)

### Código Transformador Extraído

#### A_01 - Importación y Limpieza Básica
**Transformaciones:**
1. Carga `Leads.csv` desde `02_datos/01_Originales/`
2. Eliminación de registros con nulos en `visitas_total`, `paginas_vistas_visita` (123 registros)
3. Imputación de scores (`score_actividad`, `score_perfil`) con ceros en usuarios nuevos
4. Creación de variable `usuario_nuevo` (binaria: 0/1)
5. Split stratificado train/validation 70/30 sin leakage

**Registros procesados:** 9,093 → 8,970 → 6,279 (split train)

#### A_02 - Calidad de Datos
**Transformaciones:**
1. Carga de dataset postlimpieza
2. Imputación de `fuente` con "Unknown" (16 nulos)
3. Imputación de `ambito` con "Not Specified" (1,017 nulos)
4. Imputación de `ocupacion` con "Not Provided" (1,908 nulos)
5. Eliminación de columnas sin varianza:
   - `conociste_revista` (100% "No")
   - `conociste_youtube` (100% "No")
   - `no_llamar` (99.98% "No")

**Dataset resultante:** 6,279 registros × 21 columnas

#### A_04 - Preparación de Datos
**Transformaciones:**
1. **MinMaxScaler** (rango [0,1]) aplicado a:
   - `visitas_total_mms`
   - `tiempo_en_site_total_mms`
   - `paginas_vistas_visita_mms`
   - `score_actividad_mms`
   - `score_perfil_mms`

2. **OneHotEncoding** (drop='first') aplicado a:
   - `origen` → 3 dummies
   - `fuente` → 16 dummies
   - `ult_actividad` → 15 dummies
   - `ambito` → 19 dummies
   - `ocupacion` → 6 dummies
   - `descarga_lm` → 1 dummy
   - **Total: 60 features binarios**

3. **Variables sin transformación:**
   - `usuario_nuevo` (ya binaria)
   - `tiene_score_actividad` (ya binaria)
   - `tiene_score_perfil` (ya binaria)

4. **Variables aisladas** (reinserción post-modelización):
   - `id` (clave primaria)
   - `no_enviar_email` (variable de exclusión)

**Dataset resultante:** 6,279 registros × 67 columnas (1 target + 66 features)

#### A_05 - Preselección de Features
**Transformaciones:**
1. Cálculo de importancia usando `mutual_info_classif`
2. Selección top 26 features basada en información mutua
3. Eliminación de features de baja relevancia

**Features finales:** 26 (de 66)

#### A_07 - Modelización
**Transformaciones:**
1. **StandardScaler** aplicado en CV (dentro de RandomizedSearchCV)
2. **Logistic Regression L2** entrenado con:
   - 5-fold StratifiedKFold
   - RandomizedSearchCV (30 iteraciones)
   - Métrica: roc_auc
   
3. **Hiperparámetros finales:** 
   - C = (óptimo según GridSearch)
   - penalty = 'l2'
   - solver = 'lbfgs'

4. **Métricas de desempeño:**
   - AUC-ROC: **0.8898** ✅
   - Accuracy: 82.16%
   - Precision: 79.01%
   - Recall: 70.28%
   - F1-Score: 0.7439

---

## FASE 2 — LIMPIEZA Y ENFOQUE EN MODELO FINAL (Completada)

### Decisiones de Limpieza

El notebook `08_Preproduccion.ipynb` contiene:
- ✅ **Solo código REAL** de A_01..A_07 (sin pseudo-código ni ejemplos)
- ✅ **Sin celdas markdown** excepto títulos de secciones
- ✅ **Sin prints decorativos** (solo verificaciones críticas)
- ✅ **Sin análisis exploratorio** (EDA removido)
- ✅ **Código mínimo ejecutable:** Carga → Limpieza → Preparación → Preselección → Modelización
- ✅ **Modelo exacto:** Logistic Regression con L2, hiperparámetros del ganador

### Elementos Preservados (Requeridos por A_09)

```python
var_ohe = ['origen', 'fuente', 'ult_actividad', 'ambito', 'ocupacion', 'descarga_lm']
var_bin = ['no_enviar_email', 'conociste_google', 'conociste_periodico', 'conociste_facebook', 'conociste_referencias']
num_escalar = ['visitas_total', 'tiempo_en_site_total', 'paginas_vistas_visita', 'score_actividad', 'score_perfil']
```

**Motivo:** A_09 necesita estas listas para construir el `ColumnTransformer` en el pipeline de producción.

### Transformaciones de Fila
- ✅ Eliminación de nulos críticos (FASE 1, A_01)
- ✅ Imputación de valores faltantes (FASE 1, A_01/A_02)
- ✅ Comentadas con `# --- transformaciones de fila ---`

### Transformaciones de Columna
- ✅ MinMaxScaler preservado con fit en training
- ✅ OneHotEncoder preservado con fit en training
- ✅ Variables de agrupación explícitas para ColumnTransformer

### Train/Test Split
- ✅ StratifiedKFold(5) para CV preservado
- ✅ Variables `X_selected`, `y` claramente definidas

### GridSearch
- ✅ `param_grid` completo preservado
- ✅ `RandomizedSearchCV` con 30 iteraciones preservado
- ✅ Mejor modelo instanciado explícitamente con hiperparámetros ganadores

---

## FASE 3 — GENERACIÓN DEL MANIFIESTO (Completada)

Archivo generado: `00_manifiesto_preproduccion.json`

Contiene:
- ✅ Versión y timestamp
- ✅ Ruta al CSV original
- ✅ Lista de features finalistas (26)
- ✅ Variable objetivo (`compra`)
- ✅ Modelo final (Logistic Regression L2)
- ✅ Hiperparámetros óptimos
- ✅ DAG de transformaciones con dependencias

---

## Resumen de Archivos Generados

| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| `08_Preproduccion.ipynb` | `03_notebooks/` | Notebook finalista integrado y limpio |
| `00_resumen_limpieza.md` | `07_despliegue/pre-produccion/` | Este archivo (auditoría legible) |
| `00_manifiesto_preproduccion.json` | `07_despliegue/pre-produccion/` | Contrato máquina-legible para A_09 |

---

## Próximos Pasos

**Fase 4 - Finalización:**
1. ✅ Archivos generados
2. ⏳ Usuario ejecuta `08_Preproduccion.ipynb` para validación
3. ⏳ A_09 consume manifiesto y genera scripts de producción

**Nota para usuario:** El notebook está listo para ejecutar. No necesita modificaciones. Después de la ejecución:
- Los artefactos del modelo se guardarán en `06_resultados/Modelizacion/`
- A_09 usará `00_manifiesto_preproduccion.json` para generar `07_despliegue/01_reentrenamiento.py` y `07_despliegue/02_produccion_scoring.py`

---

**Estado:** ✅ A_08_Limpieza COMPLETADA
