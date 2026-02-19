def get_inventory_tools():
	return [
		{
			"type": "function",
			"function": {
				"name": "get_product_stock",
				"description": "Consulta el stock actual y mínimo de un producto por su SKU",
				"parameters": {
					"type": "object",
					"properties": {
						"sku": {
							"type": "string",
							"description": "El código SKU del producto"
						}
					},
					"required": ["sku"]
				}				
			}
		}
	]
