import os
import sqlite3
from collections import defaultdict
from pathlib import Path


class InMemoryMemoryService:
    """
    Simple short-term memory storage.

    This version stores memories only while the Python process is running.
    It is useful for quick tests but does not persist after backend restart.
    """

    def __init__(self) -> None:
        self._memories: dict[str, list[str]] = defaultdict(list)

    def add_memory(self, chat_id: str, memory: str) -> None:
        memory = memory.strip()

        if not memory:
            return

        if memory not in self._memories[chat_id]:
            self._memories[chat_id].append(memory)

    def get_recent_memories(self, chat_id: str, limit: int = 5) -> list[str]:
        memories = self._memories.get(chat_id, [])
        return memories[-limit:]

    def clear_memory(self, chat_id: str) -> None:
        self._memories[chat_id] = []


class SQLiteMemoryService:
    """
    Persistent SQLite memory storage.

    Memories are saved into a local SQLite database file, so they survive
    backend restarts.

    Table:
    - id
    - chat_id
    - memory
    - created_at

    The combination of chat_id + memory is unique to avoid exact duplicates.
    """

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = Path(
            db_path or os.getenv("MEMORY_DB_PATH", "data/agent_memory.sqlite3")
        )

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT NOT NULL,
                    memory TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(chat_id, memory)
                )
                """
            )
            connection.commit()

    def add_memory(self, chat_id: str, memory: str) -> None:
        memory = memory.strip()

        if not chat_id.strip() or not memory:
            return

        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO memories (chat_id, memory)
                VALUES (?, ?)
                """,
                (chat_id, memory),
            )
            connection.commit()

    def get_recent_memories(self, chat_id: str, limit: int = 5) -> list[str]:
        if not chat_id.strip():
            return []

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT memory
                FROM memories
                WHERE chat_id = ?
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (chat_id, limit),
            ).fetchall()

        memories = [row["memory"] for row in rows]

        # Reverse so the oldest of the recent memories appears first.
        return list(reversed(memories))

    def clear_memory(self, chat_id: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                DELETE FROM memories
                WHERE chat_id = ?
                """,
                (chat_id,),
            )
            connection.commit()

    def get_all_memories(self, chat_id: str) -> list[str]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT memory
                FROM memories
                WHERE chat_id = ?
                ORDER BY created_at ASC, id ASC
                """,
                (chat_id,),
            ).fetchall()

        return [row["memory"] for row in rows]
