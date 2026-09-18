import pandas as pd
from pathlib import Path


def load_tickets():
    data_path = (
        Path(__file__).parent.parent
        / "data"
        / "support_tickets.csv"
    )

    df = pd.read_csv(data_path)

    return df