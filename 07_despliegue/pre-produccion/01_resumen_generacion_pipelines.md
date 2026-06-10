# Generación de Pipelines sklearn - Fase 9 (A_09)

**Agente:** A_09_PreProduccion_Codigos  
**Timestamp:** 2026-06-09  
**Estado:** ✅ COMPLETADO

---

## Archivos Generados

### 1. `07_despliegue/01_reentrenamiento.py`

**Objetivo:** Entrenar modelo con búsqueda de hiperparámetros y generar artefacto.

**Componentes:**
- **Carga de datos:** CSV original desde `02_datos/01_Originales/Leads.csv`
- **Preparación:** Función `prepara_datos(df)` con transformaciones de filas:
  - Eliminación de nulos críticos (visitas_total, paginas_vistas_visita)
  - Imputación de scores y creación de usuario_nuevo
  - Imputación de categóricas (fuente, ambito, ocupacion)
  - Eliminación de columnas sin varianza

- **Pipeline sklearn:**
  ```
  ColumnTransformer(
    - MinMaxScaler: [visitas_total, tiempo_en_site_total, paginas_vistas_visita, score_actividad, score_perfil]
    - OneHotEncoder: [origen, fuente, ult_actividad, ambito, ocupacion, descarga_lm]
    - FunctionTransformer: [conociste_google, conociste_periodico, conociste_facebook, conociste_referencias]
    - FunctionTransformer: [usuario_nuevo]
  ) + LogisticRegression
  ```

- **Búsqueda de hiperparámetros:**
  - Estrategia: RandomizedSearchCV (n_iter=30)
  - CV: StratifiedKFold (n_splits=5, shuffle=True)
  - Métrica: roc_auc
  - Parámetro a buscar: C ∈ [0.001, 0.01, 0.1, 1, 10, 100]
  - Otros: penalty='l2', solver='lbfgs', max_iter=1000

- **Salida:**
  - Mejor pipeline serializado en: `07_despliegue/artefacto_pipeline.pkl` (cloudpickle)
  - Métricas de validación impresas (AUC-ROC, Accuracy, Precision, Recall, F1)

**Ejecución:**
```bash
cd C:\Users\robin\dev\01_LEADSCORING
python 07_despliegue\01_reentrenamiento.py
```

---

### 2. `07_despliegue/02_produccion_scoring.py`

**Objetivo:** Generar predicciones en datos nuevos usando pipeline entrenado.

**Componentes:**
- **Argumentos CLI:**
  - `--input`: Ruta CSV de entrada (datos para scoring)
  - `--output`: Ruta CSV de salida (con predicciones)

- **Flujo:**
  1. Carga CSV de entrada
  2. Aplica `prepara_datos(df)` (idéntica a 01_reentrenamiento.py)
  3. Carga artefacto_pipeline.pkl
  4. Ejecuta `predict_proba(X)` y `predict(X)`
  5. Genera CSV de salida con columnas: `id`, `prediction` (0/1), `probability` (0-1)

- **Validaciones:**
  - Verifica que artefacto existe antes de intentar cargar
  - Imprime estadísticas de predicciones (proporción positiva, rango de probabilidades)

**Ejecución:**
```bash
cd C:\Users\robin\dev\01_LEADSCORING
python 07_despliegue\02_produccion_scoring.py --input datos_nuevos.csv --output resultados_scoring.csv
```

---

## Características del Diseño

### ✅ Pipeline-First
- Toda la lógica de transformación en `ColumnTransformer` + `make_pipeline`
- Separación clara entre transformaciones de filas (prepara_datos) y columnas (pipeline)

### ✅ Transformers Nativos sklearn
- MinMaxScaler para normalización numérica
- OneHotEncoder con drop='first' y handle_unknown='ignore'
- FunctionTransformer para conversiones simples (binarias)

### ✅ Flujo Lineal
- Sin `main()` ni `if __name__ == "__main__"`
- Imports → Constantes → Funciones → Pipeline → Búsqueda → Guardado
- Ejecución directa desde línea de comandos o como módulo

### ✅ Búsqueda de Hiperparámetros
- Encapsulada en el pipeline completo
- RandomizedSearchCV con 30 iteraciones
- Métrica: roc_auc (del manifiesto)
- Refit=True: mejor pipeline ya está reentrenado

### ✅ Sin Dependencias Nuevas
- Librerías: pandas, numpy, sklearn, cloudpickle (todas ya usadas en proyecto)
- No introduce nuevas dependencias externas

---

## Validación Estática

### 01_reentrenamiento.py
- ✅ `make_column_transformer()` presente
- ✅ `make_pipeline()` presente
- ✅ `RandomizedSearchCV` aplicado al pipeline
- ✅ NO contiene `def main(` ni `if __name__ == "__main__"`
- ✅ Lógica lineal, sin main()

### 02_produccion_scoring.py
- ✅ Carga artefacto con `cloudpickle.load()`
- ✅ Llamadas a `predict()` y `predict_proba()`
- ✅ NO contiene `fit()` ni variantes de entrenamiento
- ✅ NO contiene `def main(` ni `if __name__ == "__main__"`
- ✅ Lógica lineal, sin main()

---

## Próximos Pasos

1. **Ejecutar reentrenamiento:**
   ```bash
   python 01_reentrenamiento.py
   ```
   Esto generará `artefacto_pipeline.pkl` con el mejor modelo encontrado.

2. **Usar en producción:**
   ```bash
   python 02_produccion_scoring.py --input nuevos_leads.csv --output predicciones.csv
   ```

3. **Fase 10:** Validación con datos reservados (validation.pkl)

---

## Variables de Agrupación (Documentación)

```python
var_ohe = ['origen', 'fuente', 'ult_actividad', 'ambito', 'ocupacion', 'descarga_lm']
var_bin = ['conociste_google', 'conociste_periodico', 'conociste_facebook', 'conociste_referencias']
num_escalar = ['visitas_total', 'tiempo_en_site_total', 'paginas_vistas_visita', 'score_actividad', 'score_perfil']
var_sin_transform = ['usuario_nuevo']
variables_aisladas = ['id', 'no_enviar_email']  # Removidas para modelado, reinsertadas después
```

---

## Notas Técnicas

1. **ColumnTransformer y remainder='drop':** Ignora columnas no especificadas (variables aisladas)
2. **OneHotEncoder con drop='first':** Evita multicolinealidad perfecta (variable dummy trap)
3. **handle_unknown='ignore':** Maneja categorías nuevas en producción sin errores
4. **FunctionTransformer:** Convierte binarias categóricas (Yes/No → 1/0) compatible con pipeline
5. **cloudpickle:** Serializa el pipeline completo, incluyendo transformers y modelo
6. **StratifiedKFold:** Mantiene proporciones de clases en cada fold (importante para datos desbalanceados)
