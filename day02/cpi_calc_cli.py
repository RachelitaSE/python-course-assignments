import pandas as pd
import datetime
import os


def load_cpi_data(excel_file: str) -> pd.DataFrame:
    """
    Loads CPI data from the given Excel file.
    The file must contain columns: date, cpi
    """
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file '{excel_file}' not found.")
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        raise RuntimeError(f"Could not read Excel file '{excel_file}': {e}")

    # Ensure required columns exist
    if "date" not in df.columns or "cpi" not in df.columns:
        raise ValueError("Excel file must contain 'date' and 'cpi' columns.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "cpi"])
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
# Command-line interface
# ==========================
def get_valid_date(prompt: str) -> datetime.date:
    """Prompt the user until a valid date is entered."""
    while True:
        date_str = input(prompt).strip()
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("⚠️  Invalid date format. Please use YYYY-MM-DD (e.g., 2015-07-01).")


def get_valid_float(prompt: str) -> float:
    """Prompt until a valid number is entered."""
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("⚠️  Please enter a valid numeric amount (e.g., 10000).")


if __name__ == "__main__":
    print("CPI Adjustment Calculator")
    print("----------------------------")

    # Get Excel file
    excel_file = input("Enter Excel filename (default: cpi_data.xlsx): ").strip()
    if not excel_file:
        excel_file = "cpi_data.xlsx"

    # Validate file exists
    if not os.path.exists(excel_file):
        print(f"File '{excel_file}' not found. Please make sure it's in the same folder.")
        exit(1)

    # Get user inputs safely
    amount = get_valid_float("Enter the amount to adjust (e.g., 10000): ")
    date_from = get_valid_date("Enter start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter end date (YYYY-MM-DD): ")

    try:
        df = load_cpi_data(excel_file)
        adjusted_value = adjust_cpi(df, amount, date_from, date_to)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    print("\n============================")
    print(f"Original amount: {amount:,.2f} ILS")
    print(f"From: {date_from}")
    print(f"To:   {date_to}")
    print(f"Adjusted (CPI): {adjusted_value:,.2f} ILS")
    print("============================")
