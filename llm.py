"""LLM Configuration for Google Gemini"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def get_gemini_llm(temperature=0, model="gemini-1.5-flash"):
    """Initialize and return Gemini LLM"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=api_key,
        convert_system_message_to_human=True
    )


def get_structured_llm(pydantic_model, temperature=0):
    """Get LLM with structured output"""
    llm = get_gemini_llm(temperature=temperature, model="gemini-1.5-flash")
    return llm.with_structured_output(pydantic_model)
