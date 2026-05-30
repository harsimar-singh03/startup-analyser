from langgraph.graph import StateGraph, END

from state import StartupState

from nodes.supervisor_node import supervisor_node
from nodes.tool_executor_node import tool_executor_node
from nodes.reflection_node import reflection_node

builder = StateGraph(StartupState)

builder.add_node("supervisor",supervisor_node)
builder.add_node("tool_executor",tool_executor_node)
builder.add_node("reflection",reflection_node)


builder.set_entry_point("supervisor")
builder.add_edge("supervisor","tool_executor")
builder.add_edge("tool_executor","reflection")

def reflection_router(state):
    if state["next_action"] == "FINISHED":
        return END

    return "supervisor"



builder.add_conditional_edges("reflection",reflection_router)

graph = builder.compile()
