import pandas as pd
import datetime
import os
import tkinter as tk
from tkinter import messagebox, filedialog

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
            raise ValueError(f"No CPI data found for {month_start.strftime('%Y-%m')}")
        return float(self.df.loc[month_start, "cpi"])

    def adjust(self, amount: float, date_from: datetime.date, date_to: datetime.date) -> float:
        if date_to < date_from:
            raise ValueError("End date must be later than start date")

        cpi_from = self.get_cpi(date_from)
        cpi_to = self.get_cpi(date_to)
        adjusted = amount * (cpi_to / cpi_from)
        return round(adjusted, 2)


# ---------------------------
# GUI Implementation
# ---------------------------
class CPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 CPI Adjustment Calculator")
        self.root.geometry("420x320")
        self.root.resizable(False, False)

        self.excel_file = tk.StringVar(value="cpi_data_fixed.xlsx")

        # --- UI Elements ---
        tk.Label(root, text="CPI Excel File:").pack(pady=(15, 0))
        tk.Entry(root, textvariable=self.excel_file, width=40).pack()
        tk.Button(root, text="Browse", command=self.browse_file).pack(pady=(0, 10))

        tk.Label(root, text="Amount (ILS):").pack()
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=(0, 10))

        tk.Label(root, text="Start Date (YYYY-MM-DD):").pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.pack(pady=(0, 10))

        tk.Label(root, text="End Date (YYYY-MM-DD):").pack()
        self.end_entry = tk.Entry(root)
        self.end_entry.pack(pady=(0, 10))

        tk.Button(root, text="Calculate", command=self.calculate).pack(pady=(10, 5))

        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="green")
        self.result_label.pack(pady=10)

    def browse_file(self):
        """Let user select an Excel file."""
        filename = filedialog.askopenfilename(
            title="Select CPI Excel File",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        if filename:
            self.excel_file.set(filename)

    def calculate(self):
        """Perform CPI adjustment."""
        try:
            excel_file = self.excel_file.get().strip()
            amount = float(self.amount_entry.get().strip())
            date_from = datetime.datetime.strptime(self.start_entry.get().strip(), "%Y-%m-%d").date()
            date_to = datetime.datetime.strptime(self.end_entry.get().strip(), "%Y-%m-%d").date()

            adjuster = CPIAdjusterExcel(excel_file)
            adjusted_value = adjuster.adjust(amount, date_from, date_to)

            self.result_label.config(
                text=f"{amount:,.2f} ILS from {date_from}\n"
                     f"is worth {adjusted_value:,.2f} ILS in {date_to}",
                fg="green"
            )

        except FileNotFoundError as e:
            messagebox.showerror("File Error", str(e))
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CPIApp(root)
    root.mainloop()
