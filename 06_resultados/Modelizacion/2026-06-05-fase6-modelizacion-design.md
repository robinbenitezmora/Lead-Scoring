---
title: Fase 6 - Modelización para Lead Scoring
date: 2026-06-05
status: Design Approved
---

# FASE 6: DISEÑO DE MODELIZACIÓN

## Objetivo
Entrenar modelos predictivos para Lead Scoring con target AUC ≥ 0.80, manteniendo balance entre interpretabilidad y precisión.

## Decisiones Clave

### Estrategia de Modelos
- **Modelo Interpretable:** Regresión Logística L2 (análisis de coeficientes)
- **Modelo Experimental:** XGBoost (maximizar precisión predictiva)
- **Justificación:** Balance pragmático - uno explicable para negocio, otro para validar potencial de AUC

### Validación
- **Método:** Validación Cruzada 5-Fold Estratificado en training set
- **Prueba Final:** Evaluación en `validation.pkl` (datos reservados, sin leakage)
- **Métricas:** ROC-AUC (primario), Precision, Recall, F1

### Interpretabilidad
- **Logistic Regression:** Análisis completo de coeficientes (top features +/-)
- **XGBoost:** Solo AUC reportado (sin permutation importance ni SHAP)
- **Restricción:** Seguir especificación de análisis con solo coeficientes

### Datos
- **Input:** `05_train_tablon_preseleccion.pkl` (6,279 × 27: 26 features + target)
- **Validación:** `validation.pkl` (2,691 registros, no usado en entrenamiento)
- **Variables Aisladas:** `04_train_variables_aisladas.pkl` (id, no_enviar_email - sincronizadas si es necesario)

## Flujo de Ejecución

### Paso 1: Carga y Preparación
```
1. Cargar 05_train_tablon_preseleccion.pkl
2. Extraer X (26 features), y (target)
3. Validar: 6,279 registros, 0 nulos, distribución 37% conversión
```

### Paso 2: Validación Cruzada (5-Fold)
```
Para cada fold (i=1..5):
  - Split estratificado en X_train_fold, X_val_fold, y_train_fold, y_val_fold
  - Entrenar Logistic Regression(penalty='l2', solver='lbfgs')
  - Entrenar XGBoost(scale_pos_weight=1.7, max_depth=6, learning_rate=0.1)
  - Evaluar: ROC-AUC, Precision, Recall, F1 en val_fold
  - Guardar métricas
Reportar: promedio ± desv.est de métricas CV
```

### Paso 3: Entrenamiento Final
```
Usar hiperparámetros óptimos encontrados en CV
- Entrenar Logistic Regression en TODO el training set
- Entrenar XGBoost en TODO el training set
- Guardar modelos: logistic_regression_model.pkl, xgboost_model.pkl
```

### Paso 4: Evaluación en Validation Set
```
Cargar validation.pkl (datos nunca vistos)
Para cada modelo:
  - Predecir probabilidades (predict_proba)
  - Calcular ROC-AUC, Precision, Recall, F1
  - Comparar con resultados CV (validación de overfitting)
  - Generar matriz de confusión y curva ROC
```

### Paso 5: Análisis de Interpretabilidad
```
SOLO LOGISTIC REGRESSION:
  - Extraer coeficientes (modelo.coef_[0])
  - Ordenar por magnitud absoluta
  - Top 10 positivos (aumentan probabilidad de compra)
  - Top 10 negativos (disminuyen probabilidad)
  - Visualización: gráfico horizontal de coeficientes

XGBOOST:
  - Sin análisis (modelo de referencia)
  - Solo reportar AUC alcanzado
```

## Salidas

### Notebook
- **Archivo:** `03_notebooks/06_Modelizacion.ipynb`
- **Contenido:** Código ejecutable, gráficos, resultados de CV

### Reporte Markdown
- **Archivo:** `06_resultados/Modelizacion/Reporte_Modelizacion.md`
- **Estructura:**
  1. Resumen Ejecutivo (AUC alcanzado, modelo recomendado)
  2. Metodología (CV, métricas, restricciones)
  3. Resultados CV (tabla 5-fold)
  4. Resultados Validation Set (comparativa)
  5. Análisis de Coeficientes (Logistic Regression)
  6. Validación de Overfitting (CV vs Validation)
  7. Conclusiones

### Modelos Guardados
- `06_resultados/Modelizacion/logistic_regression_model.pkl`
- `06_resultados/Modelizacion/xgboost_model.pkl`
- `06_resultados/Modelizacion/cv_results.json` (métricas detalladas)

## Restricciones y Supuestos

### Restricciones
- ❌ NO usar permutation importance (solo coeficientes)
- ❌ NO usar balanceo de clases (mantener distribución natural 37/63)
- ❌ NO usar `validation.pkl` en entrenamiento (solo evaluación final)

### Supuestos
- Dataset preseleccionado ya tiene 0 nulos
- Multicolinealidad controlada (r < 0.90)
- 26 features tienen poder predictivo validado por RFECV

## Métricas de Éxito

| Criterio | Objetivo | Status |
|----------|----------|--------|
| ROC-AUC (Validation) | ≥ 0.80 | TBD |
| Diferencia CV vs Validation | < 0.05 | TBD |
| Logistic Regression es interpretable | Sí | ✅ (por diseño) |
| Ambos modelos evaluados en validation.pkl | Sí | ✅ (por diseño) |

## Próximos Pasos Post-Modelización

1. Evaluar si AUC ≥ 0.80 alcanzado
2. Seleccionar modelo final (Logistic Regression si AUC suficiente, else XGBoost)
3. Fase 7: Scoring y Ranking (merge predicciones con variables aisladas)
4. Fase 8: Exportación de leads para operaciones

---

**Creado:** 2026-06-05  
**Autor:** Claude Code  
**Estado:** Listo para Implementación
