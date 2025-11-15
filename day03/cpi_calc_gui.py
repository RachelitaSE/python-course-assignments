import pandas as pd
import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox


# ==========================
# CPI Adjustment Functions
# ==========================

def load_cpi_data(excel_file: str) -> pd.DataFrame:
    """Loads CPI data from the given Excel file."""
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
    """Returns the CPI value for the month of the given date (or the last available before it)."""
    month_start = pd.Timestamp(date.year, date.month, 1)
    if month_start not in df.index:
        prev = df.loc[:month_start]
        if not prev.empty:
            return float(prev["cpi"].iloc[-1])
        raise ValueError(f"No CPI data found for {month_start.strftime('%Y-%m')}")
    return float(df.loc[month_start, "cpi"])


def adjust_cpi(df: pd.DataFrame, amount: float, date_from: datetime.date, date_to: datetime.date) -> float:
    """Adjusts an amount according to CPI between two dates."""
    if date_to < date_from:
        raise ValueError("End date must be later than start date")
    cpi_from = get_cpi(df, date_from)
    cpi_to = get_cpi(df, date_to)
    return round(amount * (cpi_to / cpi_from), 2)


# ==========================
# GUI Logic (No Classes)
# ==========================

def browse_file():
    filename = filedialog.askopenfilename(
        title="Select CPI Excel File",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
    )
    if filename:
        excel_file_var.set(filename)


def calculate():
    try:
        excel_file = excel_file_var.get().strip()
        if not excel_file:
            raise ValueError("Please select an Excel file.")

        amount = float(amount_var.get().strip())
        date_from = datetime.datetime.strptime(start_var.get().strip(), "%Y-%m-%d").date()
        date_to = datetime.datetime.strptime(end_var.get().strip(), "%Y-%m-%d").date()

        df = load_cpi_data(excel_file)
        adjusted_value = adjust_cpi(df, amount, date_from, date_to)

        result_label.config(
            text=(
                f"Original: {amount:,.2f} ILS\n"
                f"From: {date_from}\n"
                f"To:   {date_to}\n"
                f"Adjusted (CPI): {adjusted_value:,.2f} ILS"
            ),
            fg="green"
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))


# ==========================
# Main GUI Setup
# ==========================
root = tk.Tk()
root.title("CPI Adjustment Calculator")
root.geometry("540x300")
root.configure(padx=20, pady=15)

# Variables
excel_file_var = tk.StringVar(value="cpi_data.xlsx")
amount_var = tk.StringVar()
start_var = tk.StringVar()
end_var = tk.StringVar()

# Row 0 – Excel file
tk.Label(root, text="Excel File:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=4)
tk.Entry(root, textvariable=excel_file_var, width=40).grid(row=0, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=5)

# Row 1 – Amount
tk.Label(root, text="Amount (ILS):", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=4)
tk.Entry(root, textvariable=amount_var, width=20).grid(row=1, column=1, sticky="w", pady=4)

# Row 2 – Initial date
tk.Label(root, text="Initial Date (YYYY-MM-DD):", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=4)
tk.Entry(root, textvariable=start_var, width=20).grid(row=2, column=1, sticky="w", pady=4)

# Row 3 – Final date
tk.Label(root, text="Final Date (YYYY-MM-DD):", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=4)
tk.Entry(root, textvariable=end_var, width=20).grid(row=3, column=1, sticky="w", pady=4)

# Row 4 – Button
tk.Button(root, text="Calculate", command=calculate, bg="#0078D7", fg="white", width=15).grid(
    row=4, column=1, pady=12, sticky="w"
)

# Row 5 – Result label (multi-line display)
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="green",
                        wraplength=480, justify="left", anchor="w")
result_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(5, 0))

# Adjust geometry to ensure all lines visible
root.update_idletasks()
root.mainloop()
