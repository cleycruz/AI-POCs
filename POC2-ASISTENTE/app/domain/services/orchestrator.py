import json
from app.schemas.inventory import AnalisisStock # Nuestro Pydantic de respuesta

class InventoryOrchestrator:
    def __init__(self, openai_client, sql_repo, search_repo):
        self.openai = openai_client
        self.sql = sql_repo
        self.search = search_repo

    def run(self, user_query: str):
        # 1. Recuperar contexto de los manuales (RAG - Blob Storage)
        # Lo hacemos primero para que la IA tenga las "reglas del juego"
        doc_context = self.search.get_relevant_context(user_query)

        # 2. Primera llamada a OpenAI para analizar la intención
        messages = [
            {"role": "system", "content": f"Eres un asistente logístico experto. Contexto de manuales: {doc_context}"},
            {"role": "user", "content": user_query}
        ]
        
        # Obtenemos las definiciones de las herramientas (Fase 3.B)
        from app.infrastructure.openai.tools_definition import get_inventory_tools
        
        response = self.openai.get_completion(
            messages=messages, 
            tools=get_inventory_tools()
        )
        
        message = response.choices[0].message
        tool_calls = message.tool_calls

        # 3. Si la IA decide que necesita SQL (Function Calling)
        if tool_calls:
            for tool_call in tool_calls:
                if tool_call.function.name == "get_product_stock":
                    # Extraer el SKU que la IA identificó
                    args = json.loads(tool_call.function.arguments)
                    
                    # LLAMADA AL REPOSITORIO SQL (Infraestructura)
                    product_data = self.sql.get_stock_by_sku(args['sku'])
                    
                    # Añadir la respuesta de la DB al hilo de conversación
                    messages.append(message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "get_product_stock",
                        "content": str(product_data)
                    })

            # 4. Segunda llamada a OpenAI para consolidar SQL + RAG
            final_response = self.openai.get_completion(messages=messages)
            return final_response.choices[0].message.content

        return message.content