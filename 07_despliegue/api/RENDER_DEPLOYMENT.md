# Configuración de Despliegue en Render

## Información General

Esta API FastAPI está lista para ser desplegada en Render como Web Service.

**Tipo de Servicio:** Web Service  
**Tipo de Stack:** Python  
**Root Directory:** `07_despliegue/api`

---

## Configuración de Render

### 1. Parámetros Obligatorios

| Parámetro | Valor |
|-----------|-------|
| **Root Directory** | `07_despliegue/api` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn api.main:app --host 0.0.0.0 --port $PORT --app-dir ..` |

### 2. Variables de Entorno

| Clave | Valor |
|-------|-------|
| `PYTHON_VERSION` | `3.13.9` |

**Nota:** Configurar manualmente en el dashboard de Render, en la sección `Environment`.

---

## Flujo de Despliegue Manual

### Paso 1: Commit y Push a GitHub

```bash
git add 07_despliegue/api/
git commit -m "Fase 10 ✅: API FastAPI lista para Render"
git push origin main
```

### Paso 2: Alta en Render Dashboard

1. Ir a https://render.com
2. Crear **New → Web Service**
3. Conectar repositorio GitHub
4. Configurar:
   - **Name:** lead-scoring-api (o nombre preferido)
   - **Repository:** robinbenitezmora/Lead-Scoring
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT --app-dir ..`

### Paso 3: Configurar Variables de Entorno

En el dashboard de Render, sección **Environment:**

```
PYTHON_VERSION=3.13.9
```

### Paso 4: Deploy

Hacer clic en **Create Web Service** y esperar a que Render construya e inicie el servicio.

---

## Validación Post-Deploy

Una vez que Render indique que el servicio está **Running**, probar:

### Health Check
```bash
curl https://lead-scoring-api.onrender.com/health
```

Respuesta esperada:
```json
{"status": "OK", "service": "lead-scoring-api"}
```

### Debug
```bash
curl https://lead-scoring-api.onrender.com/debug
```

### Predict (con payload)
```bash
curl -X POST https://lead-scoring-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '[{"id": 1, "origen": "API", "fuente": "Chat", ...}]'
```

---

## Troubleshooting

### Error: `Module not found: uvicorn`
- **Causa:** requirements.txt no se instaló
- **Solución:** Verificar que `Build Command` es `pip install -r requirements.txt`

### Error: `AttributeError: 'LogisticRegression' object has no attribute 'multi_class'`
- **Causa:** Versión de scikit-learn incompatible con el artefacto
- **Solución:** Regenerar artefacto con `01_reentrenamiento.py` usando `PYTHON_VERSION=3.13.9`

### Error: `FileNotFoundError: artefacto_pipeline.pkl`
- **Causa:** Artefacto no se copió a `07_despliegue/api/`
- **Solución:** Verificar que `artefacto_pipeline.pkl` existe en `07_despliegue/api/`

### Servicio tarda mucho en responder o timeout
- **Causa:** El plan Hobby de Render suspende servicios inactivos
- **Solución:** Usar plan pagado o ejecutar en local

---

## Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/debug` | Diagnóstico del motor |
| POST | `/predict` | Inferencia principal |
| GET | `/docs` | Documentación interactiva (Swagger UI) |

---

## Contrato de API

### Request (POST /predict)

```json
[
  {
    "id": 123,
    "origen": "API",
    "fuente": "Chat",
    "ult_actividad": "Page Visited on Website",
    "ambito": "Select",
    "ocupacion": "Unemployed",
    "descarga_lm": "No",
    "conociste_google": "No",
    "conociste_periodico": "No",
    "conociste_facebook": "No",
    "conociste_referencias": "No",
    "visitas_total": 5,
    "tiempo_en_site_total": 100,
    "paginas_vistas_visita": 2.5,
    "score_actividad": 15,
    "score_perfil": 15,
    "usuario_nuevo": 0
  }
]
```

### Response (200 OK)

```json
{
  "predicciones": [
    {
      "id": 123,
      "prediction": 1,
      "probability": 0.8234,
      "canal": "comercial"
    }
  ],
  "total_registros": 1
}
```

**Campo `canal` (Lógica de Negocio):**
- `"autogestión"` → probability < 0.40 (leads fríos, bajo potencial)
- `"automatización"` → 0.40 ≤ probability < 0.70 (leads tibios, potencial moderado)
- `"comercial"` → probability ≥ 0.70 (leads calientes, alto potencial)

---

## Próximos Pasos

1. **Verificar que la API funciona en local:** `uvicorn api.main:app --reload --app-dir ..`
2. **Hacer commit y push a GitHub**
3. **Alta en Render dashboard** siguiendo los pasos anteriores
4. **Validar endpoints en producción**

---

**Última actualización:** 2026-06-09  
**Estado:** ✅ Listo para Render
