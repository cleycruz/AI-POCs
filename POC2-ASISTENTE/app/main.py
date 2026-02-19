from fastapi import FastAPI, Depends, HTTPException
from app.core.config import settings
from app.domain.services.orchestrator import InventoryOrchestrator
from app.infrastructure.openai.openai_client import OpenAIClient
from app.infrastructure.database.sql_repository import SQLInventoryRepository
from app.infrastructure.search.search_repository import SearchRepository
from app.schemas.chat import ChatRequest

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# --- FÁBRICA DE DEPENDENCIAS ---
# Esto asegura que los clientes se reutilicen (Singleton-ish)
openai_client = OpenAIClient()
sql_repo = SQLInventoryRepository()
search_repo = SearchRepository()

def get_orchestrator():
    return InventoryOrchestrator(openai_client, sql_repo, search_repo)

# --- ENDPOINTS ---

@app.get("/")
def health_check():
    return {"status": "online", "service": settings.PROJECT_NAME}

@app.post("/api/v1/query")
async def process_inventory_query(
    request: ChatRequest, 
    orchestrator: InventoryOrchestrator = Depends(get_orchestrator)
):
    """
    Endpoint principal para las consultas de los gerentes de VASS
    """
    try:
        response = orchestrator.run(request.query)
        return {"answer": response}
    except Exception as e:
        # Aquí conectarías con app.core.telemetry para loguear en App Insights
        raise HTTPException(status_code=500, detail=f"Error procesando la consulta: {str(e)}")