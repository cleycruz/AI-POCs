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
- Usa variables de entorno para secretos y nunca subas .env al repositorio.
- Agrega más tests para lógica de negocio y endpoints (ya tienes estructura y dependencias para pytest y pytest-asyncio).
- Usa Application Insights para monitoreo en producción (ya integrado en el arranque de la app).
- Mantén requirements.txt actualizado y compatible con la versión de Python usada (actualmente 3.12).
- La infraestructura es reproducible y parametrizada con Terraform, permitiendo despliegues multiambiente.
- Los recursos de Azure (Search, SQL, Application Insights, Storage) están alineados con la lógica del backend.
- Los outputs de Terraform facilitan la integración de endpoints y claves en la configuración de la app.
- El código está modularizado y desacoplado (domain, infrastructure, core, schemas, main).
- Manejo de errores y logs implementado para trazabilidad.
- Documentación clara y actualizada.

## Ejemplo de uso de la API

### Healthcheck
```http
GET /health
```
Respuesta:
```json
{"status": "ok"}
```

### Consulta de inventario (ejemplo)
```http
POST /api/v1/query
{
	"query": "¿Cuánto stock hay del producto X?"
}
```
Respuesta esperada:
```json
{
	"respuesta": "Actualmente hay 120 unidades del producto X en inventario.",
	"contexto": "Fuente: inventario2026.xlsx ..."
}
```

## Infraestructura y despliegue

- Toda la infraestructura se define en `/POC2-ASISTENTE/terraform/` usando buenas prácticas de variables, outputs y recursos alineados con el backend.
- Puedes desplegar todo el stack con:
	```bash
	cd POC2-ASISTENTE/terraform
	terraform init
	terraform apply
	```
- Los outputs te darán los endpoints y claves para tu .env.

## Recomendaciones adicionales

- Si el proyecto crece, considera separar los módulos de infraestructura en subcarpetas.
- Puedes agregar scripts de automatización para exportar outputs de Terraform a tu .env.
- Mantén la documentación y los tests siempre actualizados.
