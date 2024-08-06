import json
import logging
import time
from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.schemas.example import Example
from src.services.logger import Logger
from src.services.config import Config

logger = Logger(name="VectorDataBase").get_logger()


class VectorDataBase:
    def __init__(self, config: Config) -> None:
        logger.info("Starting VectorDataBase...")
        self.dataset_path = (
            Path(__file__).parents[1] / "data" / config.get("examples_dataset_file")
        )
        self.model_name = config.get("embeddings_model_name")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        self.collection_name = config.get("vdb_collection")
        self.url = config.get("vdb_api_url")

        # self.embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = QdrantVectorStore.from_existing_collection(
            url=self.url,
            collection_name=self.collection_name,
            embedding=self.embedding_model,
        )
        logger.info("VectorDatabase started")

    def create(self) -> None:
        """Create the vector database with initial examples"""
        logger.info("Creating vectorstore...")
        start_t = time.time()
        examples_json = json.loads(open(self.dataset_path, "r").read())
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
        logger.info(f"Vectorstore created in {time.time() - start_t} seconds!")

    def search(self, text: str, n: int = 10) -> list[str]:
        """Perform the semantic search given a text"""
        logger.info(f"Searching vectorstore for: {text}")
        returned_docs = self.vectorstore.similarity_search(text, k=n)
        logger.info(f"Found examples: {returned_docs}")
        return returned_docs

    def update(self, examples: list[str]) -> None:
        """Update the knownledge database with new examples"""
        logger.info(f"Updating vectorstore with examples: {examples}")
        return None
