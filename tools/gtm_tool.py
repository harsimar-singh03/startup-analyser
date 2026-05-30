from utils.groq_client import llm

def gtm_strategy_tool(startup_idea: str):


    prompt = f"""
    You are a startup go-to-market strategist.

    Startup Idea:
    {startup_idea}

    Create a go-to-market strategy.

    Include:
    - target audience
    - launch strategy
    - customer acquisition
    - marketing channels
    - first 90 day plan

    Keep it practical and actionable.

    IMPORTANT:

        * Keep response between 200 to 300 words
    """

    response = llm.invoke(prompt)
    print("2:gtm_strategy_tool")
    return {
        "tool_name": "gtm_strategy_tool",
        "summary": response.content
    }

