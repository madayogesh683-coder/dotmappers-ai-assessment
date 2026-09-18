import pandas as pd


def detect_anomalies(df: pd.DataFrame):
    results = []

    # 1. Abnormally long resolution times
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

    # 2. Unresolved high-priority tickets older than 24 hours
    if (
        "created_at" in df.columns
        and "priority" in df.columns
        and "status" in df.columns
    ):
        data = df.copy()

        data["created_at"] = pd.to_datetime(
            data["created_at"],
            errors="coerce"
        )

        # Use the latest ticket timestamp as the reference point.
        # This makes the detection reproducible.
        reference_time = data["created_at"].max()

        unresolved = ~data["status"].astype(str).str.lower().isin(
            ["resolved", "closed"]
        )

        high_priority = data["priority"].astype(str).str.lower().isin(
            ["high", "critical"]
        )

        older_than_24h = (
            (reference_time - data["created_at"])
            > pd.Timedelta(hours=24)
        )

        old_unresolved = data[
            unresolved & high_priority & older_than_24h
        ]

        for _, ticket in old_unresolved.iterrows():
            age_hours = (
                reference_time - ticket["created_at"]
            ).total_seconds() / 3600

            results.append({
                "ticket_id": ticket["ticket_id"],
                "type": "Unresolved high-priority ticket",
                "details": (
                    f"{ticket['priority']} priority ticket is "
                    f"{age_hours:.1f} hours old and has status "
                    f"{ticket['status']}"
                )
            })

    return results