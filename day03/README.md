# 🧮 CPI Adjustment Calculator — Day 03

This project adjusts a monetary amount based on changes in the **Consumer Price Index (CPI)** between two dates where the  business logic is separated from the user interface and a test file added.
---

## 📁 Folder Contents


| `cpi_logic.py` | Contains the *business logic* (functions to load data, get CPI, and adjust values). |
| `cpi_calc_cli.py` | Command-line interface — lets you enter an amount and dates interactively. |
| `test_cpi_logic.py` | Test suite for `cpi_logic.py`, using `pytest`. |
| `cpi_data.xlsx` | Excel file with CPI data — must include columns `date` and `cpi`. |

---

## ⚙️ Installation

make sure you have pandas openpyxl pytest installed. If not:

`pip3 install pandas openpyxl pytest`

Run the interactive calculator from your terminal:

```python3 cpi_calc_cli.py```

Then follow the prompts:

```
CPI Adjustment Calculator
----------------------------
Enter Excel filename (default: cpi_data.xlsx):
Enter the amount: 10000
Enter start date (YYYY-MM-DD): 2020-01-01
Enter end date (YYYY-MM-DD): 2021-01-01

Adjusted amount: 11,000.00 ILS
```
Then run tests:
All logic tests are written using pytest.

`pytest -v`

The output should look like:
```
============================= test session starts =============================
collected 4 items

test_cpi_logic.py::test_get_cpi_valid PASSED
test_cpi_logic.py::test_get_cpi_invalid PASSED
test_cpi_logic.py::test_adjust_cpi_increase PASSED
test_cpi_logic.py::test_adjust_cpi_reverse_dates PASSED
============================== 4 passed in 0.02s ==============================
```