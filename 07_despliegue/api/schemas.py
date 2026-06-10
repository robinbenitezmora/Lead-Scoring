"""
Contrato oficial de entrada y salida de la API de scoring ML.

RegistroEntrada: 16 campos obligatorios derivados del flujo real de 02_produccion_scoring.py
ScoringSalida: respuesta completa del motor (id, prediction, probability)
"""

from pydantic import BaseModel, Field
from typing import List


class RegistroEntrada(BaseModel):
    """Contrato externo oficial de entrada a la API."""

    id: int = Field(..., description="Identificador único del registro")
    origen: str = Field(..., description="Origen del contacto (p.ej. API, Landing Page Submission)")
    fuente: str = Field(..., description="Fuente de adquisición (p.ej. Chat, Organic Search)")
    ult_actividad: str = Field(..., description="Última actividad registrada (p.ej. Page Visited on Website)")
    ambito: str = Field(..., description="Ámbito de aplicación (p.ej. Select, Business Administration)")
    ocupacion: str = Field(..., description="Ocupación del contacto (p.ej. Unemployed, Student)")
    descarga_lm: str = Field(..., description="Descarga de lead magnet (Yes/No)")

    conociste_google: str = Field(..., description="Conoció vía Google (Yes/No)")
    conociste_periodico: str = Field(..., description="Conoció vía Periódico (Yes/No)")
    conociste_facebook: str = Field(..., description="Conoció vía Facebook (Yes/No)")
    conociste_referencias: str = Field(..., description="Conoció vía Referencias (Yes/No)")

    visitas_total: int = Field(..., description="Total de visitas al sitio")
    tiempo_en_site_total: int = Field(..., description="Tiempo total en sitio (segundos)")
    paginas_vistas_visita: float = Field(..., description="Páginas vistas por visita")
    score_actividad: int = Field(..., description="Score de actividad [0-20]")
    score_perfil: int = Field(..., description="Score de perfil [0-20]")
    usuario_nuevo: int = Field(..., description="Es usuario nuevo (0/1)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 660737,
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
                "visitas_total": 0,
                "tiempo_en_site_total": 0,
                "paginas_vistas_visita": 0.0,
                "score_actividad": 15,
                "score_perfil": 15,
                "usuario_nuevo": 0
            }
        }


class PrediccionSalida(BaseModel):
    """Contrato de salida individual para un registro."""

    id: int = Field(..., description="Identificador del registro")
    prediction: int = Field(..., description="Predicción binaria (0=No compra, 1=Compra)")
    probability: float = Field(..., description="Probabilidad de compra [0.0, 1.0]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 660737,
                "prediction": 0,
                "probability": 0.1782
            }
        }


class RespuestaPredicciones(BaseModel):
    """Respuesta de la API de predicción (lista de resultados)."""

    predicciones: List[PrediccionSalida] = Field(
        ...,
        description="Lista de predicciones para los registros enviados"
    )
    total_registros: int = Field(..., description="Total de registros procesados")

    class Config:
        json_schema_extra = {
            "example": {
                "predicciones": [
                    {
                        "id": 660737,
                        "prediction": 0,
                        "probability": 0.1782
                    },
                    {
                        "id": 660728,
                        "prediction": 0,
                        "probability": 0.3245
                    }
                ],
                "total_registros": 2
            }
        }
