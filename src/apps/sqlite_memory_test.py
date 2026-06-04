from src.services.memory import SQLiteMemoryService


def main() -> None:
    chat_id = "sqlite-persistence-test"
    db_path = "data/sqlite_memory_test.sqlite3"

    print("Creating first memory service...")
    memory_service_1 = SQLiteMemoryService(db_path=db_path)
    memory_service_1.clear_memory(chat_id)
    memory_service_1.add_memory(chat_id, "User likes robotics and PCB design.")

    print("Memory from first service:")
    print(memory_service_1.get_recent_memories(chat_id))

    print("\nCreating second memory service using the same database...")
    memory_service_2 = SQLiteMemoryService(db_path=db_path)

    print("Memory from second service:")
    print(memory_service_2.get_recent_memories(chat_id))

    assert memory_service_2.get_recent_memories(chat_id) == [
        "User likes robotics and PCB design."
    ]

    print("\nSQLite memory persistence test passed.")


if __name__ == "__main__":
    main()
