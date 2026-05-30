from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
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

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_secret("GROQ_API_KEY"),
    temperature=0
)