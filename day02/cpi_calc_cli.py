import pandas as pd
import datetime
import os

class CPIAdjusterExcel:
    def __init__(self, excel_file: str):
        """
        Loads CPI data from the given Excel file.
        The file must contain columns: date, cpi
        """
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f" Excel file '{excel_file}' not found.")
        try:
            self.df = pd.read_excel(excel_file)
        except Exception as e:
            raise RuntimeError(f" Could not read Excel file '{excel_file}': {e}")

        # Ensure required columns exist
        if "date" not in self.df.columns or "cpi" not in self.df.columns:
            raise ValueError(" Excel file must contain 'date' and 'cpi' columns.")

        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df = self.df.dropna(subset=["date", "cpi"])
        self.df.set_index("date", inplace=True)
        self.df.sort_index(inplace=True)

    def get_cpi(self, date: datetime.date) -> float:
        """
        Returns the CPI value for the month of the given date.
        """
        month_start = pd.Timestamp(date.year, date.month, 1)
        if month_start not in self.df.index:
            raise ValueError(f"No CPI data found for {month_start.strftime('%Y-%m')}")
        return float(self.df.loc[month_start, "cpi"])

    def adjust(self, amount: float, date_from: datetime.date, date_to: datetime.date) -> float:
        """
        Adjusts an amount according to CPI between two dates.
        """
        if date_to < date_from:
            raise ValueError("End date must be later than start date")

        cpi_from = self.get_cpi(date_from)
        cpi_to = self.get_cpi(date_to)

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
    print(" CPI Adjustment Calculator")
    print("----------------------------")

    # Get Excel file
    excel_file = input("Enter Excel filename (default: cpi_data_fixed.xlsx): ").strip()
    if not excel_file:
        excel_file = "cpi_data.xlsx"

    # Validate file exists
    if not os.path.exists(excel_file):
        print(f" File '{excel_file}' not found. Please make sure it's in the same folder.")
        exit(1)

    # Get user inputs safely
    amount = get_valid_float("Enter the amount to adjust (e.g., 10000): ")
    date_from = get_valid_date("Enter start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter end date (YYYY-MM-DD): ")

    try:
        adjuster = CPIAdjusterExcel(excel_file)
        adjusted_value = adjuster.adjust(amount, date_from, date_to)
    except Exception as e:
        print(f" Error: {e}")
        exit(1)

    print("\n============================")
    print(f"Original amount: {amount:,.2f} ILS")
    print(f"From: {date_from}")
    print(f"To:   {date_to}")
    print(f"Adjusted (CPI): {adjusted_value:,.2f} ILS")
    print("============================")
