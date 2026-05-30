from utils.groq_client import llm

def pricing_analysis_tool(startup_idea: str):


    prompt = f"""
    You are a startup pricing strategist.

    Startup Idea:
    {startup_idea}

    Your task:
    - Suggest the best pricing model
    - Suggest pricing tiers
    - Explain why

    Include:
    - pricing strategy
    - target customer
    - recommended pricing
    - monetization advice

    Keep it practical and concise.

    IMPORTANT:

        * Keep response between 200 to 300 words
    """

    response = llm.invoke(prompt)
    print("5:pricing_analysis_tool")

    return {
        "tool_name": "pricing_analysis_tool",
        "summary": response.content
    }

