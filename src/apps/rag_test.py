from src.services.rag import ChromaRAGService


def main() -> None:
    rag = ChromaRAGService()

    print(f"Chroma collection document count: {rag.get_collection_count()}")

    test_queries = [
        "What brand colors should you use?",
        "What rules should you follow for SVG or vector graphics?",
        "Tell me Nova's backstory.",
    ]

    for query in test_queries:
        print("\n" + "=" * 100)
        print(f"QUERY: {query}")

        results = rag.retrieve(query, top_k=3)

        for index, result in enumerate(results, start=1):
            print("\n" + "-" * 80)
            print(f"RESULT {index}")
            print(result)


if __name__ == "__main__":
    main()
