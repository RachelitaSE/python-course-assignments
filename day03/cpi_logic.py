# cpi_logic.py
import pandas as pd
import datetime
import os


def load_cpi_data(excel_file: str) -> pd.DataFrame:
    """Loads CPI data from an Excel file (must have columns: date, cpi)."""
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file '{excel_file}' not found.")
    df = pd.read_excel(excel_file)
    if "date" not in df.columns or "cpi" not in df.columns:
        raise ValueError("Excel file must contain 'date' and 'cpi' columns.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "cpi"])
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)
    return df


def get_cpi(df: pd.DataFrame, date: datetime.date) -> float:
    """Returns the CPI for the given month."""
    month_start = pd.Timestamp(date.year, date.month, 1)
    if month_start not in df.index:
        raise ValueError(f"No CPI data found for {month_start.strftime('%Y-%m')}")
    return float(df.loc[month_start, "cpi"])


def adjust_cpi(df: pd.DataFrame, amount: float, date_from: datetime.date, date_to: datetime.date) -> float:
    """Adjusts an amount using CPI between two dates."""
    if date_to < date_from:
        raise ValueError("End date must be later than start date")
    cpi_from = get_cpi(df, date_from)
    cpi_to = get_cpi(df, date_to)
    return round(amount * (cpi_to / cpi_from), 2)
