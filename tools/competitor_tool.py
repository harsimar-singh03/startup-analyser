import streamlit as st

from tavily import TavilyClient
from dotenv import load_dotenv
from utils.groq_client import llm

import os

load_dotenv()

def get_secret(key):
    value = os.getenv(key)
    if value:
        return value
    try:
        return st.secrets[key]
    except:
        return None

client = TavilyClient(api_key=get_secret("TAVILY_API_KEY"))

def competitor_scan_tool(startup_idea: str):


    query = f"""
    Top competitors, pricing, features,
    weaknesses and market leaders for:
    {startup_idea}
    """

    search_result = client.search(
        query=query,
        search_depth="advanced",
        max_results=3
    )

    search_content = ""

    for result in search_result["results"]:

        search_content += f"""
        TITLE:
        {result['title']}

        CONTENT:
        {result['content']}
        """

    prompt = f"""
    You are a startup competitor analyst.

    Based on this research:

    {search_content}

    Create:
    - Top competitors
    - Their strengths
    - Their weaknesses
    - Market gaps
    - Business opportunities

    Keep it clean and structured.

    IMPORTANT:

        * Keep response between 200 to 300 words
        

    """

    response = llm.invoke(prompt)
    print("1:competitor_scan_tool")

    return {
        "tool_name": "competitor_scan_tool",
        "summary": response.content
    }

