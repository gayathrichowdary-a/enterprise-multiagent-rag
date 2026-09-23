def memory_node(state):
    memory_store = MemoryStore()

    matches = memory_store.search_memory(
        state["query"]
    )

    if not matches:
        recent_memory = memory_store.get_recent_memory(limit=3)

        if recent_memory:
            memory_context = "Recent conversation history:\n"

            for item in recent_memory:
                memory_context += (
                    f"\nUser: {item['query']}\n"
                    f"Assistant: {item['response']}\n"
                )
        else:
            memory_context = ""

    else:
        memory_context = "Relevant previous conversation:\n"

        for item in matches:
            memory_context += (
                f"\nUser: {item['query']}\n"
                f"Assistant: {item['response']}\n"
            )

    state["memory_context"] = memory_context

    return state