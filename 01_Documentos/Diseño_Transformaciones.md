# Diseño de Transformaciones — Lead Scoring Project

**Fecha**: 2026-06-04  
**Objetivo del proyecto**: Regresión Logística para clasificación binaria (Lead Scoring)  
**Target**: compra (BINARIO 0/1 - conversión sí/no)  
**Modelos priorizados**: Regresión Logística (Logistic Regression)  
**Estado**: ✅ CONGELADO Y APLICADO (todas las transformaciones realizadas)

---

## Estrategia para Regresión Logística

✅ **StandardScaler**: Mejora convergencia del optimizador  
✅ **Log en variables sesgadas**: Normaliza distribuciones  
✅ **OneHotEncoder (drop='first')**: Evita multicolinealidad perfecta  
✅ **Target sin transformar**: Se mantiene binario (0/1)

---

## Transformaciones Aplicadas

### FASE 1: Numéricas (8 features)
- Log + StandardScaler: visitas_total, tiempo_en_site_total, paginas_vistas_visita
- StandardScaler: score_actividad, score_perfil, usuario_nuevo, tiene_score_actividad, tiene_score_perfil

### FASE 2: Categóricas (41 dummies OHE)
- origen (3), fuente (4), ult_actividad (7), ambito (19), ocupacion (6)
- descarga_lm (1), no_enviar_email (1)

---

## Riesgos y Consideraciones para Logística

⚠️ **Dimensionalidad**: 50 features para 6,279 observaciones (ratio 126:1)  
⚠️ **ambito con 19 dummies**: Considerar regularización L1/L2  
⚠️ **Posible colinealidad**: Validar con matriz de correlación  

**Mitigaciones**:
- Usar solver='lbfgs' o 'liblinear' con penalty='l2' por defecto
- Considerar max_iter=5000 para convergencia
- Monitorear log-loss durante entrenamiento

---

**Aplicación completada**: 2026-06-04  
**Dataframe final**: 04_train_tablon_transformado.pkl (6,279 × 50)
