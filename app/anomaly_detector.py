import pandas as pd


def detect_anomalies(df: pd.DataFrame):
    results = []

    # Convert created_at to datetime
    df = df.copy()
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # --------------------------------------------------
    # 1. Abnormally long resolution times
    # --------------------------------------------------
    if "resolution_time_hrs" in df.columns:
        long_tickets = df[
            df["resolution_time_hrs"].notna()
            & (df["resolution_time_hrs"] > 48)
        ]

        for _, ticket in long_tickets.iterrows():
            results.append({
                "ticket_id": ticket["ticket_id"],
                "type": "Long resolution time",
                "details": (
                    f"Resolution took "
                    f"{ticket['resolution_time_hrs']} hours"
                )
            })

    # --------------------------------------------------
    # 2. Unresolved high-priority tickets older than 24 hours
    # --------------------------------------------------
    if "priority" in df.columns and "status" in df.columns:

        reference_time = df["created_at"].max()

        unresolved_high_priority = df[
            (df["priority"].astype(str).str.lower().isin(
                ["high", "critical"]
            ))
            & (df["status"].astype(str).str.lower().isin(
                ["open", "escalated"]
            ))
            & ((reference_time - df["created_at"]).dt.total_seconds() / 3600 > 24)
        ]

        for _, ticket in unresolved_high_priority.iterrows():
            age_hours = (
                reference_time - ticket["created_at"]
            ).total_seconds() / 3600

            results.append({
                "ticket_id": ticket["ticket_id"],
                "type": "Unresolved high-priority ticket",
                "details": (
                    f"{ticket['priority']} priority ticket has been "
                    f"unresolved for {age_hours:.1f} hours"
                )
            })

    return results