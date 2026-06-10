# 📊 INFORME DE PRESELECCIÓN DE VARIABLES
## Fase 5: Agente A_05_SeleccionadorVariables

**Fecha de Ejecución:** 2026-06-05  
**Método:** RFECV con Regresión Logística L1  
**Estado:** ✅ COMPLETADO

---

## 📋 RESUMEN EJECUTIVO

### Reducción de Variables
- **Variables iniciales:** 66 features
- **Variables tras RFECV L1:** 24 features (-63.6%)
- **Variables eliminadas por correlación:** 2 variables (-3.0%)
- **Variables finales:** 26 features preseleccionadas (-60.6% reducción total)

### Dataset Preseleccionado
```
Archivo: 02_datos/03_Entrenamiento/05_train_tablon_preseleccion.pkl
Registros: 6,279
Columnas: 27 (26 features + 1 target)
Nulos: 0
Tamaño: 1.4 MB
```

---

## 🎯 DECISIÓN CRÍTICA: SIN BALANCEO DE CLASES

**Distribución Natural:** 37% conversión (2,335 casos positivos)  
**Justificación:** Representatividad del caso real en producción  
**Fase de Balanceo:** ⊘ SALTADA en este proyecto  

### Implicaciones para Modelización
- Train/test split SIN balanceo
- Modelos entrenados reflejan desbalance real
- Próximo agente: A_06_Modelizador (Fase 6, no Fase 7)

---

## 📊 VARIABLES PRESELECCIONADAS (26 TOTAL)

### Distribución por Tipo

**Numéricas Escaladas (3):**
- visitas_total_mms, tiempo_en_site_total_mms, paginas_vistas_visita_mms

**Binarias (1):**
- usuario_nuevo

**Categóricas - OHE (22):**
- origen (2): Landing Page, Lead Add Form
- fuente (4): Direct Traffic, Google, Organic Search, Press_Release
- ult_actividad (8): Chat, Converted, Email Bounced, Email Link Clicked, Email Opened, Form Submitted, Phone, Page Visited, SMS
- ambito (3): Not Specified, Retail, Select
- ocupacion (4): Housewife, Not Provided, Unemployed, Working Professional

---

## ✅ VALIDACIONES REALIZADAS

- ✅ 6,279 registros preservados
- ✅ 0 valores faltantes
- ✅ Multicolinealidad controlada (r < 0.90)
- ✅ RFECV optimal features: 24
- ✅ Correlaciones eliminadas: 2

---

## 📁 ARCHIVOS GENERADOS

1. `02_datos/03_Entrenamiento/05_train_tablon_preseleccion.pkl` - Dataset preseleccionado
2. `01_Documentos/Variables_preseleccionadas.txt` - Lista de variables
3. `03_notebooks/05_Preseleccion_Variables.ipynb` - Notebook ejecutado
4. `.github/copilot-instructions.md` - Actualizado

---

**Generado:** 2026-06-05 | **Versión:** 1.0
