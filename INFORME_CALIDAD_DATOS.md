# 📊 INFORME DE CALIDAD DE DATOS

**Lead Scoring - Limpieza e Imputación de Datos**

**Fecha:** 2026-06-02
**Estado:** ✅ COMPLETADO
**Versión Dataset:** v3 (Final)

---

## 📋 TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Fase 1: Limpieza de Nulos](#fase-1-limpieza-de-nulos)
3. [Fase 2: Imputación de Scores](#fase-2-imputación-de-scores)
4. [Análisis de Resultados](#análisis-de-resultados)
5. [Archivos Generados](#archivos-generados)
6. [Próximos Pasos](#próximos-pasos)

---

## 📌 RESUMEN EJECUTIVO

### Transformaciones Realizadas

Se realizó un proceso completo de limpieza e imputación de datos en 3 versiones:

| Versión     | Registros | Columnas | Cambios Principales                   |
| ------------ | --------- | -------- | ------------------------------------- |
| **v1** | 9,093     | 23       | Original (con nulos)                  |
| **v2** | 8,970     | 23       | Eliminación de nulos críticos       |
| **v3** | 8,970     | 24       | Imputación de scores + usuario_nuevo |

### Indicadores Clave

- **Tasa de retención:** 98.65% (8,970 de 9,093 registros)
- **Registros eliminados:** 123 (1.35%)
- **Usuarios nuevos identificados:** 4,103 (45.74%)
- **Usuarios existentes:** 4,867 (54.26%)
- **Estado final:** ✅ Listo para modelado

---

## FASE 1️⃣ - LIMPIEZA DE NULOS

### Objetivo

Eliminar registros con valores faltantes en columnas críticas:

- `visitas_total`
- `paginas_vistas_visita`

### Problema Detectado

```
visitas_total:           123 nulos (1.35%)
paginas_vistas_visita:   123 nulos (1.35%)
```

### Solución Aplicada

Se eliminaron **123 registros** que tenían nulos simultáneamente en ambas columnas.

### Distribución de Registros Eliminados

```
Lead Add Form:    97 registros (78.9%)
Lead Import:      24 registros (19.5%)
API:               2 registros (1.6%)
```

### Resultado de la Fase

```
✅ visitas_total:           0 nulos
✅ paginas_vistas_visita:   0 nulos
```

**Dataset v2 Generado:**

- Registros: 8,970
- Columnas: 23
- Archivo: `df_leads_clean_v2.csv`

---

## FASE 2️⃣ - IMPUTACIÓN DE SCORES

### Objetivo

Imputar valores faltantes en variables de scoring:

- `score_actividad`
- `score_perfil`

### Problema Detectado

```
score_actividad:  4,103 nulos (45.74%)
score_perfil:     4,103 nulos (45.74%)
```

### Estrategia de Imputación

#### Segmentación Realizada

Se identificaron dos grupos de usuarios:

1. **Usuarios Existentes (usuario_nuevo = 0)**

   - Registros: 4,867 (54.26%)
   - Tienen valores en scores
   - No requieren imputación
2. **Usuarios Nuevos (usuario_nuevo = 1)**

   - Registros: 4,103 (45.74%)
   - Nulos en ambos scores
   - Imputados con valor **cero**

#### Justificación de Imputación con Ceros

- Usuarios nuevos no tienen historial de actividad
- Score = 0 representa "sin actividad"
- Mantiene diferenciación con usuarios existentes via `usuario_nuevo`
- Permite al modelo aprender patrones específicos de usuarios nuevos

### Resultados Post-Imputación

```
✅ score_actividad:  0 nulos
✅ score_perfil:     0 nulos
```

### Distribución de Scores

#### Usuarios Existentes (n=4,867)

```
score_actividad:
  • Media: 14.31 | Desv: 1.40 | Rango: [7, 18]
  
score_perfil:
  • Media: 16.35 | Desv: 1.81 | Rango: [11, 20]
```

#### Usuarios Nuevos (n=4,103)

```
score_actividad:
  • Media: 0.00 | Desv: 0.00 | Rango: [0, 0]
  
score_perfil:
  • Media: 0.00 | Desv: 0.00 | Rango: [0, 0]
```

### Variable Creada: usuario_nuevo

```
usuario_nuevo = 0:  4,867 registros (54.26%) - No imputado, con scores originales
usuario_nuevo = 1:  4,103 registros (45.74%) - Imputado, scores = 0
```

**Dataset v3 Generado:**

- Registros: 8,970
- Columnas: 24
- Archivo: `df_leads_clean_v3.csv`

---

## 📊 ANÁLISIS DE RESULTADOS

### Tasa de Conversión (Compra)

#### Usuarios Existentes

```
Compra = 0:  3,080 registros (63.28%)
Compra = 1:  1,787 registros (36.72%)
Tasa:        36.72%
```

#### Usuarios Nuevos

```
Compra = 0:  2,558 registros (62.34%)
Compra = 1:  1,545 registros (37.66%)
Tasa:        37.66%
```

### Insights Principales

1. **Distribución Balanceada de Conversión**

   - Ambos grupos tienen tasas similares (~37%)
   - No hay sesgo significativo por tipo de usuario
2. **Segmentación Efectiva**

   - Variable `usuario_nuevo` captura diferencia fundamental
   - 45.74% del dataset son usuarios nuevos
3. **Datos Listos para Modelado**

   - Sin valores faltantes críticos
   - Características bien distribuidas
   - Segmentación clara de usuarios

---

## 📁 ARCHIVOS GENERADOS

### Datasets Procesados

```
02_datos/03_Entrenamiento/
├── df_leads_clean_v2.csv (8,970 registros, 23 columnas)
│   └── Cambios: Nulos eliminados en visitas_total, paginas_vistas_visita
└── df_leads_clean_v3.csv (8,970 registros, 24 columnas)
    └── Cambios: Scores imputados + variable usuario_nuevo
```

### Logs de Transformación

```
06_resultados/
├── eda_summary.json          (Resumen de análisis exploratorio)
├── limpieza_log.json         (Log de limpieza de nulos)
└── imputacion_log.json       (Log de imputación de scores)
```

---

## 📈 VARIABLES DEL DATASET FINAL (v3)

### Variables Numéricas (10)

```
• id
• compra (Target)
• visitas_total
• tiempo_en_site_total
• paginas_vistas_visita
• score_actividad (imputado)
• score_perfil (imputado)
• tiene_score_actividad
• tiene_score_perfil
• usuario_nuevo (nuevo)
```

### Variables Categóricas (14)

```
• origen
• fuente
• no_enviar_email
• no_llamar
• ult_actividad
• ambito
• ocupacion
• conociste_google
• conociste_revista
• conociste_periodico
• conociste_youtube
• conociste_facebook
• conociste_referencias
• descarga_lm
```

---

## ✅ VALIDACIONES COMPLETADAS

- [X] Sin nulos en `visitas_total` (v2, v3)
- [X] Sin nulos en `paginas_vistas_visita` (v2, v3)
- [X] Sin nulos en `score_actividad` (v3)
- [X] Sin nulos en `score_perfil` (v3)
- [X] Variable `usuario_nuevo` creada correctamente
- [X] Distribución de datos verificada
- [X] Tasa de conversión balanceada

---

## 🎯 PRÓXIMOS PASOS RECOMENDADOS

### Fase 3: Análisis Exploratorio Actualizado

- [ ] Actualizar EDA con distribuciones de v3
- [ ] Validar poder predictivo de `usuario_nuevo`
- [ ] Análisis univariante por tipo de usuario

### Fase 4: Feature Engineering

- [ ] Transformaciones logarítmicas (tiempo_en_site)
- [ ] Variables dummy para categorías
- [ ] Interacciones relevantes usuario_nuevo × scores
- [ ] Escalado de variables numéricas

### Fase 5: Preparación Modelado

- [ ] Split train/test estratificado
- [ ] Balanceo de clases (si es necesario)
- [ ] Validación cruzada configuration
- [ ] Baseline model establishment

### Fase 6: Modelado

- [ ] Modelos iniciales (Logistic Regression, Decision Trees)
- [ ] Evaluación con métricas (AUC, precision, recall, F1)
- [ ] Hyperparameter tuning
- [ ] Feature importance analysis

---

## 📝 NOTAS TÉCNICAS

### Decisiones de Diseño

1. **Eliminación vs Imputación en Fase 1**

   - Se eligió eliminar registros (1.35%) vs imputar
   - Razón: Visitas totales y páginas vistas son variables clave de comportamiento
   - Imputación hubiera sesgado el análisis
2. **Imputación con Ceros en Fase 2**

   - Se eligió cero vs otros métodos (media, mediana)
   - Razón: Usuarios nuevos genuinamente no tienen scores
   - Cero = "sin historial de actividad"
   - Variable `usuario_nuevo` permite al modelo diferenciar
3. **Creación de usuario_nuevo**

   - Captura variable latente importante
   - Permite modelado heterogéneo por segmento
   - No es redundante con scores = 0

---

## 🔍 CONTROL DE CALIDAD

| Aspecto              | Verificación                   | Estado     |
| -------------------- | ------------------------------- | ---------- |
| Integridad Datos     | Sin nulos críticos             | ✅ PASS    |
| Registros Duplicados | Verificar en próxima fase      | ⏳ PENDING |
| Outliers             | Análisis univariante pendiente | ⏳ PENDING |
| Balanceo Clases      | Ratio 63:37 aceptable           | ✅ PASS    |
| Consistencia         | Valores dentro de rangos        | ✅ PASS    |

---

## 📊 RESUMEN FINAL

**Estado del Proyecto:** ✅ CALIDAD DE DATOS COMPLETADA

El dataset está listo para la siguiente fase de análisis exploratorio actualizado y feature engineering. Se ha logrado:

1. **Limpieza:** Eliminación selectiva de 123 registros con datos críticos faltantes
2. **Imputación:** Estrategia coherente de imputación con ceros para usuarios nuevos
3. **Segmentación:** Variable `usuario_nuevo` para identificar y modelar usuarios sin historial
4. **Documentación:** Registro completo de transformaciones realizadas

**Dataset Utilizar:** `df_leads_clean_v3.csv`

---

**Generado:** 2026-06-02 | **Versión:** 1.0
