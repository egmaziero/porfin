import json
import logging
from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.schemas.example import Example

VDB_LOCAL_PATH = Path(__file__).parents[1] / "data"
DATASET_PATH = Path(__file__).parents[1] / "data/home_schooling.json"


class VectorDataBase:
    def __init__(self, model_name=None) -> None:
        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = "intfloat/multilingual-e5-large-instruct"
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            multi_process=True,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        self.collection_name = "examples_vectorstore"
        self.url = "http://localhost:6333"

        # self.embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        try:
            self.vectorstore = QdrantVectorStore.from_existing_collection(
                url=self.url, collection_name=self.collection_name
            )
        except:
            self.vectorstore = self.create()

    def create(self) -> None:
        """Create the vector database with initial examples"""
        examples_json = json.loads(open(DATASET_PATH, "r").read())
        examples = []
        for example in examples_json:
            try:
                examples.append(Example(**example))
            except Exception as e:
                logging.error(f"Invalid examples file. Incorrect example: {example}")
                raise e

        examples_to_index = [example.model_dump() for example in examples]
        texts = [
            " ".join(example.values()) for example in examples_to_index
        ]  # TODO or keys?
        self.vectorstore = QdrantVectorStore.from_texts(
            texts=texts,
            embedding=self.embedding_model,
            metadatas=examples_json,
            url=self.url,
            collection_name=self.collection_name,
        )

    def search(self, text: str, n: int = 10) -> list[str]:
        """Perform the semantic search given a text"""
        returned_docs = self.vectorstore.similarity_search(text, k=n)

        return returned_docs

    def update(self, examples: list[str]) -> None:
        """Update the knownledge database with new examples"""
        pass
