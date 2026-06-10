"""
API FastAPI de scoring ML tabular.

Aplicación web mínima que:
  - Valida entrada con Pydantic
  - Llama al motor scoring_df(df) desde .scoring
  - Devuelve predicciones en formato JSON

Endpoints:
  - GET  /health     → health check
  - GET  /debug      → diagnóstico del motor
  - POST /predict    → inferencia (lista de registros)
"""

import sys
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import traceback
import warnings
from typing import List

warnings.filterwarnings('ignore')

# Importar motor y schemas
from .scoring import scoring_df
from .schemas import RegistroEntrada, PrediccionSalida, RespuestaPredicciones


def asignar_canal(probability: float) -> str:
    """
    Lógica de negocio: clasificar leads en canales según probabilidad de compra.

    Reglas:
      - probability < 0.40        → "autogestión" (leads fríos, bajo potencial)
      - 0.40 <= probability < 0.70 → "automatización" (leads tibios, potencial moderado)
      - probability >= 0.70        → "comercial" (leads calientes, alto potencial)

    Args:
        probability: Probabilidad de compra [0.0, 1.0]

    Returns:
        canal: str ("autogestión", "automatización", "comercial")
    """
    if probability < 0.40:
        return "autogestión"
    elif probability < 0.70:
        return "automatización"
    else:
        return "comercial"

# Crear aplicación FastAPI
app = FastAPI(
    title="Lead Scoring API",
    description="API de scoring de leads con LogisticRegression",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health():
    """Health check: verificar que la API está operativa."""
    return {"status": "OK", "service": "lead-scoring-api"}


@app.get("/test-canal", response_model=PrediccionSalida, tags=["Debug"])
def test_canal():
    """Endpoint de prueba para verificar que el campo 'canal' se serializa."""
    return PrediccionSalida(
        id=999,
        prediction=1,
        probability=0.75,
        canal=asignar_canal(0.75)
    )


@app.get("/debug", tags=["Debug"])
def debug():
    """
    Endpoint de diagnóstico: verifica que el motor de scoring está disponible.
    Intenta cargar el artefacto y hacer una prueba mínima.
    """
    try:
        from pathlib import Path
        import cloudpickle

        artefacto_path = Path(__file__).parent / "artefacto_pipeline.pkl"

        # Verificar existencia del artefacto
        if not artefacto_path.exists():
            return JSONResponse(
                status_code=500,
                content={
                    "status": "ERROR",
                    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                    "artefacto_encontrado": False,
                    "engine_error": f"Artefacto no encontrado en {artefacto_path}",
                }
            )

        # Cargar artefacto
        with open(artefacto_path, 'rb') as f:
            pipeline = cloudpickle.load(f)

        # Crear payload de prueba mínimo
        test_data = [{
            "id": 999999,
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
            "usuario_nuevo": 0,
        }]

        # Ejecutar scoring
        df_test = pd.DataFrame(test_data)
        result = scoring_df(df_test)

        # Extraer resultado y aplicar lógica de negocio
        if len(result) > 0:
            row = result.iloc[0]
            sample_output = {
                "id": int(row['id']),
                "prediction": int(row['prediction']),
                "probability": float(row['probability']),
                "canal": asignar_canal(float(row['probability']))
            }
        else:
            sample_output = None

        return {
            "status": "OK",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "artefacto_encontrado": True,
            "input_columns_detected": list(df_test.columns),
            "output_columns_detected": list(result.columns),
            "sample_output": sample_output,
            "engine_error": None,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "engine_error": str(e),
                "traceback": traceback.format_exc(),
            }
        )


@app.post("/predict", response_model=RespuestaPredicciones, tags=["Inference"])
def predict(registros: List[RegistroEntrada]):
    """
    Endpoint principal de inferencia.

    Input:
      - Lista de registros JSON [{"id": ..., "origen": ..., ...}]
      - Validados contra RegistroEntrada (Pydantic)

    Output:
      - RespuestaPredicciones con lista de predicciones

    Excepciones:
      - 400: Entrada mal formada
      - 422: No cumple schema
      - 500: Error durante inferencia
    """
    try:
        # Validación mínima
        if not registros or len(registros) == 0:
            raise ValueError("La lista de registros no puede estar vacía")

        # Convertir Pydantic a DataFrame
        datos = [r.model_dump() for r in registros]
        df_entrada = pd.DataFrame(datos)

        # Ejecutar motor de scoring
        df_salida = scoring_df(df_entrada)

        # Convertir salida a lista de diccionarios con lógica de negocio
        predicciones_list = [
            PrediccionSalida(
                id=int(row['id']),
                prediction=int(row['prediction']),
                probability=float(row['probability']),
                canal=asignar_canal(float(row['probability']))
            )
            for _, row in df_salida.iterrows()
        ]

        return RespuestaPredicciones(
            predicciones=predicciones_list,
            total_registros=len(predicciones_list)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error de validación: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante inferencia: {str(e)}\n{traceback.format_exc()}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
