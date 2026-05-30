from utils.groq_client import llm

MAX_TOOL_RETRIES = 2

def reflection_node(state):
    prompt = f"""
    Evaluate each tool output against its checklist:

    market_research_tool — must have: market size, growth rate, trends
    competitor_scan_tool — must have: competitor names, strengths, weaknesses
    persona_builder_tool — must have: 3 personas, age, goals, frustrations
    pricing_analysis_tool — must have: pricing model, tiers, prices
    gtm_strategy_tool — must have: target audience, channels, 90 day plan
    risk_analysis_tool — must have: risk types, mitigation strategies

    Completed tools: {state.get('completed_tasks')}
    Current Outputs: {state['tool_outputs']}

    If a tool's output is missing any checklist item or their content is less tahn 500 words → flag it as WEAK.
    Only reply GOOD if ALL 6 tools pass their checklist.

    Reply ONLY:
    GOOD
    or
    WEAK: tool1, tool2
    """

    response = llm.invoke(prompt)
    result = response.content.strip()

    print("-------------------Running reflection node-----------------------")


    retry_counts = state.get("tool_retry_counts", {})
    completed = state.get("completed_tasks", [])

    if result == "GOOD":
        return {
            "reflection": result,
            "next_action": "FINISHED"
        }

    # Extract weak tools
    weak_tools = result.replace("WEAK:", "").strip()
    weak_tool_list = [t.strip() for t in weak_tools.split(",")]

    # Filter out tools that already hit max retries
    actionable_tools = [
        t for t in weak_tool_list
        if retry_counts.get(t, 0) < MAX_TOOL_RETRIES
    ]

    # If all weak tools exhausted retries, move to uncompleted tools
    all_tools = [
        "market_research_tool", "competitor_scan_tool",
        "persona_builder_tool", "pricing_analysis_tool",
        "gtm_strategy_tool", "risk_analysis_tool"
    ]
    uncompleted = [t for t in all_tools if t not in completed]

    if not actionable_tools and not uncompleted:
        # Everything done or exhausted, just finish
        return {
            "reflection": result,
            "next_action": "FINISHED"
        }

    next_tools = actionable_tools if actionable_tools else uncompleted[:2]

    return {
        "reflection": result,
        "next_action": "CONTINUE",
        "selected_tools": next_tools
    }