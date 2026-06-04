import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

CHARACTER_PROFILE_PATH = SRC_DIR / "data" / "character_profile.md"
M365_DOCS_DIR = SRC_DIR / "data" / "m365_docs"

CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", "data/chroma"))
CHROMA_COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION_NAME",
    "ai_character_agent_docs",
)
MISTRAL_EMBEDDING_MODEL = os.getenv("MISTRAL_EMBEDDING_MODEL", "mistral-embed")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def load_raw_documents() -> list[Document]:
    raw_documents: list[Document] = []

    if CHARACTER_PROFILE_PATH.exists():
        raw_documents.append(
            Document(
                page_content=CHARACTER_PROFILE_PATH.read_text(encoding="utf-8"),
                metadata={
                    "source": str(CHARACTER_PROFILE_PATH),
                    "doc_type": "character_profile",
                },
            )
        )

    if M365_DOCS_DIR.exists():
        supported_files = list(M365_DOCS_DIR.glob("*.md")) + list(M365_DOCS_DIR.glob("*.txt"))

        for file_path in supported_files:
            raw_documents.append(
                Document(
                    page_content=file_path.read_text(encoding="utf-8"),
                    metadata={
                        "source": str(file_path),
                        "doc_type": "m365_style_document",
                    },
                )
            )

    if not raw_documents:
        raise FileNotFoundError(
            "No documents found. Add src/data/character_profile.md or files in src/data/m365_docs."
        )

    return raw_documents


def split_documents(raw_documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""],
    )

    split_docs = splitter.split_documents(raw_documents)

    for index, document in enumerate(split_docs):
        document.metadata["chunk_id"] = index

    return split_docs


def rebuild_chroma_index(documents: list[Document]) -> None:
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY is missing. Add it to your .env file.")

    if CHROMA_PERSIST_DIR.exists():
        print(f"Removing old Chroma index: {CHROMA_PERSIST_DIR}")
        shutil.rmtree(CHROMA_PERSIST_DIR)

    CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    embeddings = MistralAIEmbeddings(
        model=MISTRAL_EMBEDDING_MODEL,
        api_key=MISTRAL_API_KEY,
    )

    print(f"Building Chroma index in: {CHROMA_PERSIST_DIR}")
    print(f"Collection name: {CHROMA_COLLECTION_NAME}")
    print(f"Embedding model: {MISTRAL_EMBEDDING_MODEL}")
    print(f"Documents/chunks to add: {len(documents)}")

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=str(CHROMA_PERSIST_DIR),
    )

    print("Chroma vector index built successfully.")


def main() -> None:
    raw_documents = load_raw_documents()
    print(f"Loaded raw documents: {len(raw_documents)}")

    split_docs = split_documents(raw_documents)
    print(f"Created chunks: {len(split_docs)}")

    rebuild_chroma_index(split_docs)


if __name__ == "__main__":
    main()
