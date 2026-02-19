import json
import logging
from app.infrastructure.openai.tools_definition import get_inventory_tools
from app.schemas.inventory import AnalisisStock # Asegúrate de tener este import

logger = logging.getLogger("cley.orchestrator")

class InventoryOrchestrator:
    def __init__(self, openai_client, sql_repo, search_repo):
        self.openai = openai_client
        self.sql = sql_repo
        self.search = search_repo
        self.prompt_path = "app/domain/prompts/inventory_system.txt"

    def _get_system_prompt(self, doc_context: str) -> str:
        try:
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                base_prompt = f.read()
            return f"{base_prompt}\n\nCONTEXTO DE MANUALES CLEY:\n{doc_context}"
        except FileNotFoundError:
            logger.error("System prompt file not found")
            return f"Eres un asistente logístico de Cley. Contexto: {doc_context}"

    async def run(self, user_query: str):
        # 1. RAG
        doc_context = await self.search.get_relevant_context(user_query)
        
        # 2. Prompts
        system_content = self._get_system_prompt(doc_context)
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_query}
        ]
        
        # 3. Primera llamada a OpenAI
        response = await self.openai.get_completion(
            messages=messages, 
            tools=get_inventory_tools()
        )
        
        message = response.choices[0].message
        tool_calls = message.tool_calls

        # Variables para capturar datos y usarlos en el esquema Pydantic final
        sku_detectado = "N/A"
        stock_db = 0

        # 4. Procesamiento de Function Calling
        if tool_calls:
            messages.append(message)
            
            for tool_call in tool_calls:
                if tool_call.function.name == "get_product_stock":
                    args = json.loads(tool_call.function.arguments)
                    sku_detectado = args.get('sku')
                    
                    logger.info(f"Consultando SQL para SKU: {sku_detectado}")
                    product_data = await self.sql.get_stock_by_sku(sku_detectado)
                    
                    # Guardamos el stock numérico para el Pydantic final
                    stock_db = product_data.get('stock', 0) if product_data else 0
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "get_product_stock",
                        "content": json.dumps(product_data)
                    })

            # 5. Segunda llamada para consolidar la respuesta final (texto natural)
            final_response = await self.openai.get_completion(messages=messages)
            final_content = final_response.choices[0].message.content
            
            # 6. RETORNO ESTRUCTURADO (Nivel Staff Engineer)
            return AnalisisStock(
                resumen=final_content,
                sku=sku_detectado,
                cantidad_actual=stock_db,
                nivel_urgencia="ALTA" if stock_db < 10 and sku_detectado != "N/A" else "NORMAL"
            )

        # Si no hubo tool calls, devolvemos una respuesta de texto simple convertida a nuestro esquema
        return AnalisisStock(
            resumen=message.content,
            sku="N/A",
            cantidad_actual=0,
            nivel_urgencia="NORMAL"
        )