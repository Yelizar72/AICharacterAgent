import re
from pathlib import Path


class SimpleRAGService:
    """
    Simple retrieval service over character_profile.md.

    For MVP:
    - no vector database
    - keyword-overlap retrieval

    Later upgrade:
    - replace this with Chroma, Qdrant, FAISS, or another vector database
    """

    def __init__(self, profile_path: str | None = None) -> None:
        if profile_path is None:
            project_src_dir = Path(__file__).resolve().parents[1]
            profile_path = str(project_src_dir / "data" / "character_profile.md")

        self.profile_path = Path(profile_path)
        self._profile_text = self._load_profile()
        self._chunks = self._split_into_chunks(self._profile_text)

    def _load_profile(self) -> str:
        if not self.profile_path.exists():
            raise FileNotFoundError(f"Character profile not found: {self.profile_path}")

        return self.profile_path.read_text(encoding="utf-8")

    def _split_into_chunks(self, text: str, max_chars: int = 700) -> list[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        chunks: list[str] = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 2 <= max_chars:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        scored_chunks: list[tuple[int, str]] = []

        for chunk in self._chunks:
            chunk_tokens = self._tokenize(chunk)
            score = len(query_tokens.intersection(chunk_tokens))
            scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda item: item[0], reverse=True)

        results = [
            chunk
            for score, chunk in scored_chunks[:top_k]
            if score > 0
        ]

        return results

    def get_full_profile(self) -> str:
        return self._profile_text
