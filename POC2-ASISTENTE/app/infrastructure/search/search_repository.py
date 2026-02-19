from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.core.config import settings

class SearchRepository:
    def __init__(self):
        self.client = SearchClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            index_name=settings.AZURE_SEARCH_INDEX,
            credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
        )

    def get_relevant_context(self, query: str) -> str:
        """
        Busca en los documentos de Blob Storage (indexados en AI Search)
        el contenido más relevante para la duda del usuario.
        """
        results = self.client.search(search_text=query, top=3)
        
        context = ""
        for result in results:
            context += f"\nFuente: {result['metadata_storage_name']}\nContenido: {result['content']}\n"
        
        return context