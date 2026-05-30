from utils.groq_client import llm

def chat_node(state, user_question, chat_history):
    prompt = f"""
    You are a startup advisor chatbot.

    Startup Idea: {state['startup_idea']}
    Research Context: {state['tool_outputs']}

    Previous Chat History:
    {chat_history}

    User Question: {user_question}

    Instructions:
    - Use the research context
    - Use general business knowledge
    - Give practical startup advice
    - Keep answers conversational
    """

    response = llm.invoke(prompt)
    return response.content