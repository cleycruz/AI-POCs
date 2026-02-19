import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status
from azure.monitor.opentelemetry import configure_azure_monitor

from app.core.config import settings
from app.domain.services.orchestrator import InventoryOrchestrator
from app.infrastructure.openai.openai_client import OpenAIClient
from app.infrastructure.database.sql_repository import SQLInventoryRepository
from app.infrastructure.search.search_repository import SearchRepository
from app.schemas.chat import ChatRequest

# 1. OBSERVABILIDAD (Configurar antes que nada)
# Usamos settings.APPLICATIONINSIGHTS_CONNECTION_STRING que definimos en Terraform
if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
    configure_azure_monitor(connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING)

logger = logging.getLogger("cley.assistant")
logger.info(f"Starting {settings.PROJECT_NAME}...")

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# 2. CLIENTES (Singletons por módulo)
openai_client = OpenAIClient()
sql_repo = SQLInventoryRepository()
search_repo = SearchRepository()

# 3. FÁBRICA DE DEPENDENCIAS
def get_orchestrator():
    # Inyectamos los clientes en el orquestador
    return InventoryOrchestrator(openai_client, sql_repo, search_repo)

# --- ENDPOINTS ---


@app.get("/health", summary="Healthcheck", tags=["infra"])
def health_check():
    """
    Endpoint de salud para monitoreo y readiness probe.
    """
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


@app.post("/api/v1/query", summary="Consulta logística IA", tags=["logistics"])
async def process_inventory_query(
    request: ChatRequest,
    orchestrator: InventoryOrchestrator = Depends(get_orchestrator)
):
    """
    Endpoint principal para consultas logísticas. Detecta intención, consulta SQL o manuales y retorna análisis estructurado.
    """
    # Validación extra de entrada
    if not request.query or not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El campo 'query' no puede estar vacío."
        )
    try:
        response = await orchestrator.run(request.query)
        # Si la respuesta es un modelo Pydantic, serializa correctamente
        if hasattr(response, 'model_dump'):
            return response.model_dump()
        return {"answer": response}
    except ValueError as ve:
        logger.warning(f"Error de validación: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno procesando la consulta logística."
        )