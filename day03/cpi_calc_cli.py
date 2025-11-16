# cpi_calc_cli.py
import datetime
import os
from cpi_logic import load_cpi_data, adjust_cpi


def get_valid_date(prompt: str) -> datetime.date:
    while True:
        date_str = input(prompt).strip()
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("⚠️ Invalid format. Use YYYY-MM-DD.")


def get_valid_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("⚠️ Please enter a valid number.")


def main():
    print("CPI Adjustment Calculator")
    print("----------------------------")

    excel_file = input("Enter Excel filename (default: cpi_data.xlsx): ").strip() or "cpi_data.xlsx"
    if not os.path.exists(excel_file):
        print(f"File '{excel_file}' not found.")
        return

    amount = get_valid_float("Enter the amount: ")
    date_from = get_valid_date("Enter start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter end date (YYYY-MM-DD): ")

    try:
        df = load_cpi_data(excel_file)
        adjusted = adjust_cpi(df, amount, date_from, date_to)
        print(f"\nAdjusted amount: {adjusted:,.2f} ILS")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
