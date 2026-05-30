from utils.groq_client import llm

def persona_builder_tool(startup_idea: str):


    prompt = f"""
    Create 3 realistic customer personas for:

    {startup_idea}

    Include:
    - age
    - goals
    - frustrations
    - spending behavior

    IMPORTANT:

        * Keep response between 200 to 300 words
        
    """

    response = llm.invoke(prompt)
    print("4:persona_builder_tool")
    

    return {
        "tool_name": "persona_builder_tool",
        "summary": response.content
    }

