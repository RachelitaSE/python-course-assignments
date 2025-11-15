import pandas as pd
import datetime

def load_cpi_data(excel_file: str) -> pd.DataFrame:
    """
    Loads CPI data from the given Excel file.
    The file must contain columns: date, cpi
    """
    df = pd.read_excel(excel_file)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)
    return df


def get_cpi(df: pd.DataFrame, date: datetime.date) -> float:
    """
    Returns the CPI value for the month of the given date.
    """
    month_start = pd.Timestamp(date.year, date.month, 1)
    if month_start not in df.index:
        raise ValueError(f"No CPI data found for {month_start.strftime('%Y-%m')}")
    return float(df.loc[month_start, "cpi"])


def adjust_cpi(df: pd.DataFrame, amount: float, date_from: datetime.date, date_to: datetime.date) -> float:
    """
    Adjusts an amount according to CPI between two dates.
    """
    if date_to < date_from:
        raise ValueError("End date must be later than start date")

    cpi_from = get_cpi(df, date_from)
    cpi_to = get_cpi(df, date_to)

    adjusted = amount * (cpi_to / cpi_from)
    return round(adjusted, 2)


# ==========================
# Example usage
# ==========================
if __name__ == "__main__":
    cpi_df = load_cpi_data("cpi_data.xlsx")

    original_amount = 10000.0
    date_from = datetime.date(2008, 1, 1)
    date_to = datetime.date(2025, 5, 1)

    new_value = adjust_cpi(cpi_df, original_amount, date_from, date_to)
    print(f"{original_amount:,.2f} ILS from {date_from} is worth {new_value:,.2f} ILS in {date_to}.")
