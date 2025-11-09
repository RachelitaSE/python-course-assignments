import pandas as pd
import datetime
import os
import tkinter as tk
from tkinter import messagebox, filedialog

class CPIAdjusterExcel:
    def __init__(self, excel_file: str):
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"Excel file '{excel_file}' not found.")

        # Load data
        self.df = pd.read_excel(excel_file)
        if "date" not in self.df.columns or "cpi" not in self.df.columns:
            raise ValueError("Excel file must contain 'date' and 'cpi' columns.")

        # Normalize and prepare
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df = self.df.dropna(subset=["date", "cpi"])
        self.df.set_index("date", inplace=True)
        self.df.sort_index(inplace=True)

    def get_cpi(self, date: datetime.date) -> float:
        """Return CPI for the given month (if not found, use previous month)."""
        month_start = pd.Timestamp(date.year, date.month, 1)
        if month_start in self.df.index:
            return float(self.df.loc[month_start, "cpi"])
        else:
            # Fallback: use previous available CPI
            previous = self.df.loc[:month_start]
            if not previous.empty:
                return float(previous["cpi"].iloc[-1])
            raise ValueError(f"No CPI data available for {month_start.strftime('%Y-%m')} or earlier.")

    def adjust(self, amount: float, date_from: datetime.date, date_to: datetime.date) -> float:
        if date_to < date_from:
            raise ValueError("End date must be later than start date")

        cpi_from = self.get_cpi(date_from)
        cpi_to = self.get_cpi(date_to)
        adjusted = amount * (cpi_to / cpi_from)
        return round(adjusted, 2)


# ---------------------------
# GUI Application
# ---------------------------
class CPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 CPI Adjustment Calculator")
        self.root.geometry("450x360")
        self.root.resizable(False, False)

        # Variables
        self.excel_file = tk.StringVar(value="cpi_data_fixed.xlsx")

        # --- Widgets ---
        tk.Label(root, text="Select CPI Excel File:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
        frame = tk.Frame(root)
        frame.pack()
        tk.Entry(frame, textvariable=self.excel_file, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)

        # Amount input
        tk.Label(root, text="Amount (ILS):").pack(pady=(10, 0))
        self.amount_entry = tk.Entry(root, width=20)
        self.amount_entry.pack()

        # Start date input
        tk.Label(root, text="Start Date (YYYY-MM-DD):").pack(pady=(10, 0))
        self.start_entry = tk.Entry(root, width=20)
        self.start_entry.pack()

        # End date input
        tk.Label(root, text="End Date (YYYY-MM-DD):").pack(pady=(10, 0))
        self.end_entry = tk.Entry(root, width=20)
        self.end_entry.pack()

        # Calculate button
        tk.Button(root, text="Calculate", command=self.calculate, bg="#0078D7", fg="white", width=15).pack(pady=15)

        # Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="green", wraplength=400, justify="center")
        self.result_label.pack(pady=10)

    def browse_file(self):
        """Let the user pick an Excel file."""
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
            if not excel_file:
                raise ValueError("Please select an Excel file.")
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
            messagebox.showerror("Error", f"Unexpected error:\n{e}")


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CPIApp(root)
    root.mainloop()
