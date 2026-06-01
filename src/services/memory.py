from collections import defaultdict


class InMemoryMemoryService:
    """
    Simple short-term memory storage.

    For MVP:
    - memory is stored only while the backend process is running
    - each chat_id has its own memory list

    Later upgrade:
    - replace this with SQLite, PostgreSQL, or Redis
    """

    def __init__(self) -> None:
        self._memories: dict[str, list[str]] = defaultdict(list)

    def add_memory(self, chat_id: str, memory: str) -> None:
        memory = memory.strip()

        if not memory:
            return

        # Avoid exact duplicates
        if memory not in self._memories[chat_id]:
            self._memories[chat_id].append(memory)

    def get_recent_memories(self, chat_id: str, limit: int = 5) -> list[str]:
        memories = self._memories.get(chat_id, [])
        return memories[-limit:]

    def clear_memory(self, chat_id: str) -> None:
        self._memories[chat_id] = []
