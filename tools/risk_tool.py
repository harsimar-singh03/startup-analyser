from utils.groq_client import llm

def risk_analysis_tool(startup_idea: str):


    prompt = f"""
    You are a startup risk analyst.

    Startup Idea:
    {startup_idea}

    Identify:
    - business risks
    - financial risks
    - operational risks
    - market risks
    - competition risks

    Also suggest:
    - mitigation strategies

    Keep it realistic and practical.

    IMPORTANT:

        * Keep response between 200 to 300 words
    """

    response = llm.invoke(prompt)
    print("6:risk_analysis_tool")

    return {
        "tool_name": "risk_analysis_tool",
        "summary": response.content
    }

