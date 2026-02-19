# Cley Intelligent Inventory - Asistente Logístico IA

## Descripción
Asistente logístico inteligente basado en FastAPI, Azure OpenAI, SQL y Azure Cognitive Search. Implementa RAG (Retrieval-Augmented Generation) y análisis estructurado para consultas de inventario y manuales.

## Estructura principal
- **app/main.py**: API y endpoints principales
- **app/domain/services/orchestrator.py**: Orquestador de lógica IA y datos
- **app/infrastructure/**: Integraciones con OpenAI, SQL y Search
- **app/schemas/**: Esquemas Pydantic para validación y respuesta
- **test/**: Pruebas unitarias y de integración

## Instalación
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuración
Crea un archivo `.env` con tus credenciales de Azure y Application Insights:
```
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_KEY=...
AZURE_OPENAI_MODEL=gtp-4o
SQL_SERVER=...
SQL_DATABASE=...
SQL_USERNAME=...
SQL_PASSWORD=...
AZURE_SEARCH_ENDPOINT=...
AZURE_SEARCH_KEY=...
AZURE_SEARCH_INDEX=interventory-index
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

## Ejecución
```bash
uvicorn app.main:app --reload
```

## Pruebas
```bash
pytest
```

## Buenas prácticas
- Usa variables de entorno para secretos
- Agrega más tests para lógica de negocio y endpoints
- Usa Application Insights para monitoreo en producción
- Mantén requirements.txt actualizado

## Contacto
Desarrollado por el equipo de Cley. Para soporte, contacta a tu líder técnico.
