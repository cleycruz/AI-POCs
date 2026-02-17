import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

# --- ESQUEMA DE VALIDACIÓN (Pydantic) ---
# Esto valida que la respuesta tenga el formato correcto
class AnalisisRespuesta(BaseModel):
    pregunta: str
    respuesta: str = Field(min_length=10) # Forzamos a que no sea una respuesta vacía
    fuentes_encontradas: bool

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"), 
)

def ejecutar_rag(query):
    try:
        completion = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[{"role": "user", "content": query}],
            extra_body={
                "data_sources": [{
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
                        "index_name": os.getenv("AZURE_AI_SEARCH_INDEX"),
                        "authentication": {"type": "api_key", "key": os.getenv("AZURE_AI_SEARCH_KEY")},
                        # --- AJUSTES DE PRECISIÓN ---
                        "top_n_documents": 5, # Recupera los 5 mejores fragmentos en lugar de solo 3
                        "strictness": 2,      # Rango de 1 a 5. 1 es más flexible, 5 es súper estricto.
                        "query_type": "vector_semantic_hybrid", #Busca por palabra y por significado
                        # --- EMBEDINGS ---
                        "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME") # Nombre del deployment de embeddings
    }
                                            
                    }
                }]
            }
        )
        
        raw_text = completion.choices[0].message.content
        
        # Validamos con Pydantic
        validacion = AnalisisRespuesta(
            pregunta=query,
            respuesta=raw_text,
            fuentes_encontradas=len(completion.choices[0].message.context.get('citations', [])) > 0 if hasattr(completion.choices[0].message, 'context') else False
        )
        return validacion

    except ValidationError as e:
        print(f"Error de validación de datos: {e}")
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    pregunta = "¿Dame el detalle del stockId 478661?"
    resultado = ejecutar_rag(pregunta)
    if resultado:
        print(f"\n✅ VALIDADO POR PYDANTIC:")
        print(f"Respuesta: {resultado.respuesta}")
        print(f"¿Tiene fuentes?: {resultado.fuentes_encontradas}")