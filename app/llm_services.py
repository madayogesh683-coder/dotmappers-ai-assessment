import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def local_answer(question: str, df: pd.DataFrame) -> str:
    """Answer common questions directly from the CSV."""

    q = question.lower().strip()

    df = df.copy()
    df["customer_rating"] = pd.to_numeric(
        df["customer_rating"],
        errors="coerce"
    )

    # Lowest-rated agent
    if "lowest" in q and "agent" in q and "rating" in q:
        agent_ratings = (
            df.dropna(subset=["customer_rating"])
            .groupby("agent_id")["customer_rating"]
            .mean()
            .sort_values()
        )

        if not agent_ratings.empty:
            agent = agent_ratings.index[0]
            rating = agent_ratings.iloc[0]

            return (
                f"{agent} has the lowest average customer rating "
                f"at {rating:.2f}."
            )

    # Average rating by category
    if "category" in q and "rating" in q:
        category_ratings = (
            df.dropna(subset=["customer_rating"])
            .groupby("category")["customer_rating"]
            .mean()
            .sort_values()
        )

        results = []

        for category, rating in category_ratings.items():
            results.append(f"{category}: {rating:.2f}")

        return (
            "Average customer rating by category: "
            + ", ".join(results)
        )

    # Overall average rating
    if "average" in q and "rating" in q:
        rating = df["customer_rating"].mean()
        return f"The average customer rating is {rating:.2f}."

    # Open tickets
    if "open" in q and "ticket" in q:
        count = (
            df["status"]
            .astype(str)
            .str.lower()
            .eq("open")
            .sum()
        )

        return f"There are {count} open tickets."

    # Resolved tickets
    if "resolved" in q and "ticket" in q:
        count = (
            df["status"]
            .astype(str)
            .str.lower()
            .eq("resolved")
            .sum()
        )

        return f"There are {count} resolved tickets."

    # Critical tickets
    if "critical" in q and "ticket" in q:
        count = (
            df["priority"]
            .astype(str)
            .str.lower()
            .eq("critical")
            .sum()
        )

        return f"There are {count} critical tickets."

    # Total tickets
    if "total" in q or "how many tickets are there" in q:
        return f"There are {len(df)} tickets in total."

    return (
        "Gemini quota is temporarily unavailable. "
        "Please try another supported dataset question."
    )


def generate_llm_answer(question: str, df: pd.DataFrame) -> str:

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

    agent_stats = (
        df.dropna(subset=["customer_rating"])
        .groupby("agent_id")
        .agg(
            average_rating=("customer_rating", "mean"),
            ticket_count=("ticket_id", "count")
        )
        .round(2)
        .to_dict("index")
    )

    category_ratings = (
        df.dropna(subset=["customer_rating"])
        .groupby("category")["customer_rating"]
        .mean()
        .round(2)
        .to_dict()
    )

    average_rating = df["customer_rating"].mean()
    average_response = df["response_time_hrs"].mean()
    average_resolution = df["resolution_time_hrs"].mean()

    prompt = f"""
You are an AI support-ticket analytics assistant.

Answer the user's question using ONLY the dataset statistics below.

Dataset statistics:
- Total tickets: {total_tickets}
- Status counts: {status_counts}
- Priority counts: {priority_counts}
- Category counts: {category_counts}
- Average customer rating: {average_rating:.2f}
- Average response time: {average_response:.2f} hours
- Average resolution time: {average_resolution:.2f} hours

Agent statistics:
{agent_stats}

Average rating by category:
{category_ratings}

User question:
{question}

Rules:
- Use only the provided dataset statistics.
- Do not invent numbers.
- Give a concise and clear answer.
"""

    try:
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return response.output_text.strip()

    except Exception as e:
        error_text = str(e).lower()

        if "429" in error_text or "quota" in error_text:
            return local_answer(question, df)

        return f"Gemini API error: {str(e)}"