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


def market_research_tool(startup_idea: str):


    query = f"""
    Market size, trends, growth rate,
    opportunities and industry analysis for:
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
    You are a market research analyst.

    Based on this research:

    {search_content}

    Create a clean startup market analysis.

    Return:
    - Market Size
    - Growth Rate
    - Key Trends
    - Opportunities
    - Risks

    Keep it concise and clean.

    IMPORTANT:

        * Keep response between 200 to 300 words
    """

    response = llm.invoke(prompt)
    print("3:market_research_tool")

    return {
        "tool_name": "market_research_tool",
        "summary": response.content
    }

