from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4,
        google_api_key=api_key 
    )


def get_groq():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0.3
    )






