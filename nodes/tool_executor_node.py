import asyncio

from tools.tool_registry import TOOLS

MAX_TOOL_RETRIES = 2

async def run_single_tool(tool_name,startup_idea):

    tool_function = TOOLS[tool_name]
    result = tool_function(startup_idea)
    return tool_name, result


async def execute_tools_parallel(selected_tools,startup_idea):
    tasks = []
    for tool_name in selected_tools:
        if tool_name in TOOLS:
            tasks.append(run_single_tool(tool_name,startup_idea))

    results = await asyncio.gather(*tasks)
    return results


def tool_executor_node(state):
    tool_outputs = state.get("tool_outputs",{})
    completed_tasks = state.get("completed_tasks",[])
    retry_counts = state.get("tool_retry_counts",{})

    allowed_tools = []

    reflection = state.get("reflection", "")
    is_retry = reflection.startswith("WEAK")

    for tool_name in state["selected_tools"]:

        current_retry = retry_counts.get(tool_name,0)

        # Only check retry limit if this is a reflection-triggered rerun
        if is_retry:
            if current_retry >= MAX_TOOL_RETRIES:
                print(f"{tool_name} reached max retries")
                continue

            retry_counts[tool_name] = (current_retry + 1)

        allowed_tools.append(tool_name)


    results = asyncio.run(execute_tools_parallel(allowed_tools,state["startup_idea"]))

    print("----------------------running tool executor node---------------------")
    for tool_name, result in results:
        tool_outputs[tool_name] = result
        if tool_name not in completed_tasks:
            completed_tasks.append(tool_name)


    return {
        "tool_outputs": tool_outputs,
        "completed_tasks": completed_tasks,
        "tool_retry_counts": retry_counts
    }