import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings


load_dotenv()


class SimpleRAGService:
    """
    Simple keyword-based retrieval service over local project documents.

    Sources:
    - src/data/character_profile.md
    - src/data/m365_docs/*.md
    - src/data/m365_docs/*.txt

    This is kept as a fallback or debugging baseline.
    """

    def __init__(
        self,
        profile_path: str | None = None,
        m365_docs_dir: str | None = None,
    ) -> None:
        project_src_dir = Path(__file__).resolve().parents[1]

        if profile_path is None:
            profile_path = str(project_src_dir / "data" / "character_profile.md")

        if m365_docs_dir is None:
            m365_docs_dir = str(project_src_dir / "data" / "m365_docs")

        self.profile_path = Path(profile_path)
        self.m365_docs_dir = Path(m365_docs_dir)

        self._documents = self._load_documents()
        self._chunks = self._split_documents_into_chunks(self._documents)

    def _load_documents(self) -> list[tuple[str, str]]:
        documents: list[tuple[str, str]] = []

        if self.profile_path.exists():
            documents.append(
                (
                    str(self.profile_path),
                    self.profile_path.read_text(encoding="utf-8"),
                )
            )

        if self.m365_docs_dir.exists():
            supported_files = list(self.m365_docs_dir.glob("*.md")) + list(
                self.m365_docs_dir.glob("*.txt")
            )

            for file_path in supported_files:
                documents.append(
                    (
                        str(file_path),
                        file_path.read_text(encoding="utf-8"),
                    )
                )

        if not documents:
            raise FileNotFoundError(
                "No RAG documents found. Add character_profile.md or files in src/data/m365_docs."
            )

        return documents

    def _split_documents_into_chunks(
        self,
        documents: list[tuple[str, str]],
        max_chars: int = 700,
    ) -> list[tuple[str, str]]:
        chunks: list[tuple[str, str]] = []

        for source, text in documents:
            paragraphs = [
                paragraph.strip()
                for paragraph in text.split("\n\n")
                if paragraph.strip()
            ]
            current_chunk = ""

            for paragraph in paragraphs:
                if len(current_chunk) + len(paragraph) + 2 <= max_chars:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append((source, current_chunk.strip()))
                    current_chunk = paragraph + "\n\n"

            if current_chunk.strip():
                chunks.append((source, current_chunk.strip()))

        return chunks

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        scored_chunks: list[tuple[int, str, str]] = []

        for source, chunk in self._chunks:
            chunk_tokens = self._tokenize(chunk)
            score = len(query_tokens.intersection(chunk_tokens))
            scored_chunks.append((score, source, chunk))

        scored_chunks.sort(key=lambda item: item[0], reverse=True)

        results: list[str] = []

        for score, source, chunk in scored_chunks[:top_k]:
            if score > 0:
                results.append(f"Source: {source}\n{chunk}")

        return results

    def get_all_sources(self) -> list[str]:
        return sorted(set(source for source, _ in self._chunks))


class ChromaRAGService:
    """
    Vector RAG service using Chroma and Mistral embeddings.

    This class loads an existing local Chroma collection from:
    data/chroma

    To build or rebuild the index, run:
    uv run python -m src.apps.build_vector_index
    """

    def __init__(
        self,
        persist_directory: str | None = None,
        collection_name: str | None = None,
        embedding_model: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_PERSIST_DIR",
            "data/chroma",
        )
        self.collection_name = collection_name or os.getenv(
            "CHROMA_COLLECTION_NAME",
            "ai_character_agent_docs",
        )
        self.embedding_model = embedding_model or os.getenv(
            "MISTRAL_EMBEDDING_MODEL",
            "mistral-embed",
        )
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")

        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY is missing. Add it to your .env file.")

        self._embeddings = MistralAIEmbeddings(
            model=self.embedding_model,
            api_key=self.api_key,
        )

        self._vectorstore = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self._embeddings,
        )

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        if not query.strip():
            return []

        documents = self._vectorstore.similarity_search(
            query=query,
            k=top_k,
        )

        results: list[str] = []

        for document in documents:
            source = document.metadata.get("source", "unknown")
            chunk_id = document.metadata.get("chunk_id", "unknown")
            content = document.page_content

            results.append(
                f"Source: {source}\n"
                f"Chunk: {chunk_id}\n"
                f"{content}"
            )

        return results

    def get_collection_count(self) -> int:
        collection = self._vectorstore._collection
        return int(collection.count())
