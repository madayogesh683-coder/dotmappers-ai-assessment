import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_llm_answer(question: str, df: pd.DataFrame) -> str:

    # Calculate reliable information from the dataset
    total_tickets = len(df)

    status_counts = (
        df["status"]
        .astype(str)
        .str.lower()
        .value_counts()
        .to_dict()
    )

    priority_counts = (
        df["priority"]
        .astype(str)
        .str.lower()
        .value_counts()
        .to_dict()
    )

    category_counts = (
        df["category"]
        .astype(str)
        .value_counts()
        .to_dict()
    )

    average_rating = df["customer_rating"].mean()
    average_response = df["response_time_hrs"].mean()
    average_resolution = df["resolution_time_hrs"].mean()

    # Try Gemini LLM
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        try:
            client = genai.Client(api_key=api_key)

            prompt = f"""
You are an AI support-ticket analytics assistant.

Answer the user's question using ONLY the dataset information below.

Total tickets: {total_tickets}
Status counts: {status_counts}
Priority counts: {priority_counts}
Category counts: {category_counts}
Average customer rating: {average_rating:.2f}
Average response time: {average_response:.2f} hours
Average resolution time: {average_resolution:.2f} hours

User question:
{question}

Give a short, clear answer.
Do not invent information.
"""

            response = client.interactions.create(
                model="gemini-3.8-flash",
                input=prompt
            )

            return response.output_text.strip()

        except Exception as e:
            error_text = str(e).lower()

            if "rate limit" in error_text or "429" in error_text:
                return (
                    "Gemini rate limit reached temporarily. "
                    "Please try again later."
                )

            return f"Gemini temporarily unavailable: {str(e)}"

    return "Gemini API key is not configured."