from wuneed.ai.rag.extensions.extension_manager import RAGExtension
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

class QueryExpansionExtension(RAGExtension):
    def __init__(self):
        super().__init__("query_expansion")

    def preprocess(self, query: str) -> str:
        expanded_terms = []
        for word in query.split():
            synsets = wordnet.synsets(word)
            if synsets:
                expanded_terms.extend([lemma.name() for lemma in synsets[0].lemmas()])
            else:
                expanded_terms.append(word)
        return " ".join(set(expanded_terms))

extension = QueryExpansionExtension()