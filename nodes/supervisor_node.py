from utils.groq_client import llm

def supervisor_node(state):

    # If reflection already selected weak tools, use those directly
    if state.get("selected_tools") and state.get("reflection", "").startswith("WEAK"):
        return {
            "selected_tools": state["selected_tools"],
            "next_action": "CONTINUE"
        } 
    
    prompt = f"""
    You are an AI startup supervisor.

    Your job:
    - Decide which tools should run next
    - Multiple tools can run in parallel
    - Avoid rerunning completed tools unless needed
    - Return ONLY tool names separated by commas

    Available tools:
    - market_research_tool
    - competitor_scan_tool
    - persona_builder_tool
    - pricing_analysis_tool
    - gtm_strategy_tool
    - risk_analysis_tool

    Startup Idea:
    {state['startup_idea']}

    Completed Tasks:
    {state['completed_tasks']}

    

    Rules:

        * If no research exists, start with:
        market_research_tool,
        competitor_scan_tool

        * persona_builder_tool should usually
        run after market and competitor research

        * pricing_analysis_tool should run
        after personas or competitors

        * gtm_strategy_tool should run near the end

        * risk_analysis_tool should run after
        enough business understanding exists

        * Select maximum 2 tools at once

        * If enough information exists,
        return FINISHED

    """

    response = llm.invoke(prompt)
    print("----------------------running supervisor node--------------------")
    raw_response = response.content.strip()

    if raw_response == "FINISHED":

        return {
            "selected_tools": [],
            "next_action": "FINISHED",
            "messages": [raw_response]
        }

    selected_tools = [
        tool.strip()
        for tool in raw_response.split(",")
    ]

    return {
        "selected_tools": selected_tools,
        "next_action": "CONTINUE",
        "messages": [raw_response]
    }

