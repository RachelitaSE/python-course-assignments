import pandas as pd
import datetime

class CPIAdjusterExcel:
    def __init__(self, excel_file: str):
        """
        Loads CPI data from the given Excel file.
        The file must contain columns: date, cpi
        """
        self.df = pd.read_excel(excel_file)
        self.df["date"] = pd.to_datetime(self.df["date"])
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
# Example usage
# ==========================
if __name__ == "__main__":
    adjuster = CPIAdjusterExcel("cpi_data.xlsx")

    original_amount = 10000.0
    date_from = datetime.date(2008, 1, 1)
    date_to = datetime.date(2025, 5, 1)

    new_value = adjuster.adjust(original_amount, date_from, date_to)
    print(f"{original_amount:,.2f} ILS from {date_from} is worth {new_value:,.2f} ILS in {date_to}.")
