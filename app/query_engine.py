import pandas as pd


def answer_query(question: str, df: pd.DataFrame) -> str:
    question = question.lower().strip()

    # Total tickets
    if "total" in question or "how many tickets" in question:
        if "open" not in question and "closed" not in question:
            return f"There are {len(df)} total tickets."

    # Open tickets
    if "open" in question:
        count = len(df[df["status"].str.lower() == "open"])
        return f"There are {count} open tickets."

    # Closed tickets
    if "closed" in question:
        count = len(df[df["status"].str.lower() == "closed"])
        return f"There are {count} closed tickets."

    # Critical tickets
    if "critical" in question:
        count = len(df[df["priority"].str.lower() == "critical"])
        return f"There are {count} critical tickets."

    # High-priority tickets
    if "high priority" in question or "high-priority" in question:
        count = len(df[df["priority"].str.lower() == "high"])
        return f"There are {count} high-priority tickets."

    # Average customer rating
    if "average rating" in question or "customer rating" in question:
        rating = df["customer_rating"].mean()
        return f"The average customer rating is {rating:.2f}."

    return (
        "I can answer questions about open, closed, total, "
        "critical, and high-priority tickets."
    )