import pytest

from app.schemas.inventory import AnalisisStock
import pytest


def test_validar_esquema_respuesta_correcta():
    datos_ejemplo = {
        "resumen": "El stock está bajo el mínimo recomendado.",
        "sku": "PROD-123",
        "cantidad_actual": 5,
        "nivel_urgencia": "ALTA"
    }
    respuesta = AnalisisStock(**datos_ejemplo)
    assert respuesta.sku == "PROD-123"
    assert respuesta.nivel_urgencia == "ALTA"

# Test de Lógica: Alerta de Quiebre

def test_nivel_urgencia_critico():
    datos = {
        "resumen": "Agotado",
        "sku": "SKU-0",
        "cantidad_actual": 0,
        "nivel_urgencia": "CRITICAL"
    }
    respuesta = AnalisisStock(**datos)
    assert respuesta.nivel_urgencia == "CRITICAL"

# Test de integración simulado (mock de orquestador)
@pytest.mark.asyncio
async def test_orquestador_respuesta_mockeada():
    class MockOrchestrator:
        async def run(self, query):
            return AnalisisStock(
                resumen="Stock: 50 unidades",
                sku="SKU-50",
                cantidad_actual=50,
                nivel_urgencia="NORMAL"
            )
    orchestrator = MockOrchestrator()
    result = await orchestrator.run("¿Cuánto stock hay del producto 101?")
    assert result.cantidad_actual == 50
    assert result.nivel_urgencia == "NORMAL"