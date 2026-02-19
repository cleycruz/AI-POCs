import pyodbc
from app.core.config import settings
from app.domain.entities.inventory import ProductStock

class SQLInventoryRepository:
    def __init__(self):
        self.conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={settings.SQL_SERVER};"
            f"DATABASE={settings.SQL_DATABASE};"
            f"UID={settings.SQL_USERNAME};"
            f"PWD={settings.SQL_PASSWORD};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )

    def get_stock_by_sku(self, sku: str) -> ProductStock:
        """
        Consulta la base de datos y mapea el resultado a una Entidad de Dominio.
        """
        query = """
            SELECT id, sku, name, current_quantity, min_threshold, last_update 
            FROM inventory_table 
            WHERE sku = ?
        """
        
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (sku,))
                row = cursor.fetchone()
                
                if not row:
                    return None
                
                # Mapeo a la entidad de dominio que creamos antes
                return ProductStock(
                    id=row.id,
                    sku=row.sku,
                    name=row.name,
                    current_quantity=row.current_quantity,
                    min_threshold=row.min_threshold,
                    last_update=row.last_update
                )