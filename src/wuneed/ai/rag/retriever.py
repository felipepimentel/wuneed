from sentence_transformers import SentenceTransformer
from weaviate import Client
import weaviate
import nltk
from nltk.tokenize import sent_tokenize
from wuneed.ai.rag.plugin_manager import plugin_manager
from typing import List, Dict, Any
from wuneed.ai.rag.extensions.extension_manager import extension_manager

nltk.download('punkt')

class RAGRetriever:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = Client("http://localhost:8080")

    def chunk_text(self, text: str, chunk_size: int = 5) -> list[str]:
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        for sentence in sentences:
            if current_length + len(sentence.split()) > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(sentence)
            current_length += len(sentence.split())
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def add_document(self, text: str, metadata: dict):
        chunks = self.chunk_text(text)
        for i, chunk in enumerate(chunks):
            vector = self.model.encode(chunk).tolist()
            self.client.data_object.create(
                "Document",
                {"text": chunk, "chunk_index": i, **metadata},
                vector=vector
            )

    def retrieve(self, query: str, limit: int = 5, plugins: List[str] = [], extensions: List[str] = []) -> Dict[str, Any]:
        for ext_name in extensions:
            extension = extension_manager.get_extension(ext_name)
            if extension:
                query = extension.preprocess(query)

        vector = self.model.encode(query).tolist()
        result = (
            self.client.query
            .get("Document", ["text", "metadata", "chunk_index"])
            .with_near_vector({"vector": vector})
            .with_limit(limit)
            .do()
        )
        context = result["data"]["Get"]["Document"]

        processed_context = context
        plugin_results = {}

        for plugin_name in plugins:
            plugin = plugin_manager.get_plugin(plugin_name)
            if plugin:
                processed_context = plugin.process(query, processed_context)
                plugin_results[plugin_name] = processed_context

        retrieval_result = {
            "original_context": context,
            "processed_context": processed_context,
            "plugin_results": plugin_results
        }

        for ext_name in extensions:
            extension = extension_manager.get_extension(ext_name)
            if extension:
                retrieval_result = extension.postprocess(retrieval_result)

        return retrieval_result

rag_retriever = RAGRetriever()