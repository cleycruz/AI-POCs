from openai import AzureOpenAI
from app.core.config import settings

class OpenAIClient:
    def __init__(self):
        # Usamos la configuración centralizada (Fase 2: Seguridad)
        self.client = AzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_KEY,
            api_version="2024-02-15-preview"
        )

    def get_completion(self, messages, tools=None):
        """
        Llamada a GPT-4o con parámetros controlados (Fase 3: Implementación)
        """
        return self.client.chat.completions.create(
            model=settings.AZURE_OPENAI_MODEL,
            messages=messages,
            tools=tools,
            temperature=0.1,  # <--- BAJA TEMPERATURA = MENOS ALUCINACIÓN
            top_p=0.95,       # <--- CONTROL DE DIVERSIDAD
            max_tokens=800
        )