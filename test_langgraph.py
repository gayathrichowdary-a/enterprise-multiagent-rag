from langgraph_workflow.workflow import app

result = app.invoke(
    {
        "query": "What skills are in Siri resume?"
    }
)

print("\n===== FINAL ANSWER =====\n")

print(
    result["final_answer"]
)