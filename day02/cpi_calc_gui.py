import pandas as pd
import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class CPIAdjusterExcel:
    def __init__(self, excel_file: str):
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"Excel file '{excel_file}' not found.")
        self.df = pd.read_excel(excel_file)
        if "date" not in self.df.columns or "cpi" not in self.df.columns:
            raise ValueError("Excel file must contain 'date' and 'cpi' columns.")
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df = self.df.dropna(subset=["date", "cpi"])
        self.df.set_index("date", inplace=True)
        self.df.sort_index(inplace=True)

    def get_cpi(self, date: datetime.date) -> float:
        month_start = pd.Timestamp(date.year, date.month, 1)
        if month_start not in self.df.index:
            prev = self.df.loc[:month_start]
            if not prev.empty:
                return float(prev["cpi"].iloc[-1])
            raise ValueError(f"No CPI data found for {month_start.strftime('%Y-%m')}")
        return float(self.df.loc[month_start, "cpi"])

    def adjust(self, amount: float, date_from: datetime.date, date_to: datetime.date) -> float:
        if date_to < date_from:
            raise ValueError("End date must be later than start date")
        cpi_from = self.get_cpi(date_from)
        cpi_to = self.get_cpi(date_to)
        return round(amount * (cpi_to / cpi_from), 2)


class CPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPI Adjustment Calculator")
        self.root.geometry("520x260")
        self.root.configure(padx=20, pady=15)

        # Variables
        self.excel_file = tk.StringVar(value="cpi_data.xlsx")
        self.amount_var = tk.StringVar()
        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()

        # Row 0 – Excel file
        tk.Label(root, text="Excel File:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        tk.Entry(root, textvariable=self.excel_file, width=40).grid(row=0, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5)

        # Row 1 – Amount
        tk.Label(root, text="Amount (ILS):", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=4)
        tk.Entry(root, textvariable=self.amount_var, width=20).grid(row=1, column=1, sticky="w", pady=4)

        # Row 2 – Initial date
        tk.Label(root, text="Initial Date (YYYY-MM-DD):", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=4)
        tk.Entry(root, textvariable=self.start_var, width=20).grid(row=2, column=1, sticky="w", pady=4)

        # Row 3 – Final date
        tk.Label(root, text="Final Date (YYYY-MM-DD):", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=4)
        tk.Entry(root, textvariable=self.end_var, width=20).grid(row=3, column=1, sticky="w", pady=4)

        # Row 4 – Button
        tk.Button(root, text="Calculate", command=self.calculate, bg="#0078D7", fg="white", width=15).grid(
            row=4, column=1, pady=12, sticky="w"
        )

        # Row 5 – Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="green", wraplength=450, justify="left")
        self.result_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(5, 0))

        # Force geometry update (fix for macOS AquaTk)
        self.root.update_idletasks()

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select CPI Excel File",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        if filename:
            self.excel_file.set(filename)

    def calculate(self):
        try:
            excel_file = self.excel_file.get().strip()
            if not excel_file:
                raise ValueError("Please select an Excel file.")

            amount = float(self.amount_var.get().strip())
            date_from = datetime.datetime.strptime(self.start_var.get().strip(), "%Y-%m-%d").date()
            date_to = datetime.datetime.strptime(self.end_var.get().strip(), "%Y-%m-%d").date()

            adjuster = CPIAdjusterExcel(excel_file)
            adjusted_value = adjuster.adjust(amount, date_from, date_to)

            self.result_label.config(
                text=f"Original: {amount:,.2f} ILS\nFrom: {date_from}   To: {date_to}\nAdjusted (CPI): {adjusted_value:,.2f} ILS",
                fg="green"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CPIApp(root)
    root.mainloop()
