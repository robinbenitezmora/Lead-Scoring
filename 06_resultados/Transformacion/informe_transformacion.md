# Informe de Transformaciones — Lead Scoring Logística

**Fecha**: 2026-06-04  
**Proyecto**: Lead Scoring con Regresión Logística  
**Agente**: A_04_PreparadorDatos  
**Estado**: ✅ COMPLETADO

---

## 📊 RESUMEN EJECUTIVO

**Objetivo**: Transformar tablón POST-EDA (6,279 × 21) para **clasificación binaria** con regresión logística.

**Resultado**:
- ✅ 6,279 registros (100% conservados)
- ✅ ~50 features finales
- ✅ Target BINARIO (0/1, sin transformar)
- ✅ 0 NaN (integridad garantizada)
- ✅ 7 validaciones pasadas

---

## 🔄 TRANSFORMACIONES PARA LOGÍSTICA

### FASE 1: Variables Numéricas (8 features)

**Sesgadas (Log + StandardScaler)**:
- tiempo_en_site_total → tiempo_en_site_log_ss
- visitas_total → visitas_log_ss (skew=21.99)
- paginas_vistas_visita → paginas_vistas_log_ss

**Normales (StandardScaler)**:
- score_actividad → score_actividad_ss
- score_perfil → score_perfil_ss

**Binarias (StandardScaler)**:
- usuario_nuevo, tiene_score_actividad, tiene_score_perfil

### FASE 2: Categóricas (41 dummies)

OneHotEncoder con **drop='first'** (evita multicolinealidad):
- origen: 3 dummies
- fuente: 4 dummies
- ult_actividad: 7 dummies
- ambito: 19 dummies
- ocupacion: 6 dummies
- descarga_lm: 1 dummy
- no_enviar_email: 1 dummy

### FASE 3: Escalado

StandardScaler aplicado a TODAS las numéricas finales (mejora convergencia logística).

### FASE 4: Unión y Validaciones

✅ 7 validaciones críticas pasadas

---

## 📊 DATAFRAME FINAL

| Aspecto | Valor |
|---------|-------|
| Registros | 6,279 |
| Columnas | 50 |
| Target | compra (BINARIO 0/1) |
| Features numéricas | 8 |
| Features binarias | 41 |
| Nulos | 0 |

---

## ⚠️ RIESGOS PARA REGRESIÓN LOGÍSTICA

1. **Ratio feature:sample (1:126)**: Logística es resistente pero considerar regularización
2. **Alta cardinalidad en ambito (19)**: Puede dominar el modelo
3. **Posible colinealidad**: Validar matriz de correlación
4. **usuario_nuevo correlacionada con scores**: Resultado de imputación en EDA

**Recomendaciones**:
- Usar LogisticRegression(penalty='l2', max_iter=5000)
- Monitorear coeficientes en features de ambito
- Evaluar con Cross-Validation (5-fold mínimo)

---

**Status**: ✅ PREPARADO PARA MODELIZACIÓN  
**Próxima fase**: Regresión Logística con validación cruzada
