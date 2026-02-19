def get_inventory_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_product_stock",
                "description": "Utiliza esta función para obtener datos numéricos en tiempo real de la base de datos SQL. Devuelve stock disponible, ubicación en bodega y punto de reorden.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sku": {
                            "type": "string",
                            "description": "El código alfanumérico único del producto (ej. 'PROD-123', 'SKU-99'). Si el usuario menciona el nombre, intenta inferir el SKU o pide aclaración."
                        }
                    },
                    "required": ["sku"],
                    "additionalProperties": False
                }               
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_logistics_manuals",
                "description": "Consulta políticas, protocolos de seguridad y manuales de operación de Cley. Úsala para preguntas sobre 'cómo actuar', 'procedimientos' o 'normativas'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "La duda específica sobre el manual convertida en una búsqueda semántica."
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False
                }
            }
        }
    ]