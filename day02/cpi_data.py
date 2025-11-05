import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup

def fetch_cpi_data(url: str, output_file: str = "cpi_data.xlsx"):
    """
    Fetches CPI data from the Mashkantaman website and saves it to an Excel file.
    """
    print("Fetching CPI data from website...")
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    table = soup.find("table")
    if table is None:
        raise RuntimeError("Could not find CPI table on the page")

    records = []
    for row in table.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) >= 2:
            date_str = cells[0].get_text(strip=True)
            index_str = cells[1].get_text(strip=True)
            try:
                month, year = date_str.split("/")
                month = int(month)
                year = int(year)
                cpi_value = float(index_str)
                dt = datetime.date(year, month, 1)
                records.append({"date": dt, "cpi": cpi_value})
            except Exception:
                continue  # skip headers or invalid rows

    df = pd.DataFrame(records)
    df.sort_values("date", inplace=True)
    df.to_excel(output_file, index=False)

    print(f"✅ CPI data saved successfully to {output_file}")
    print(f"📈 Total records: {len(df)}")

if __name__ == "__main__":
    url = "https://mashcantaman.co.il/%D7%9E%D7%93%D7%93-%D7%94%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%9C%D7%A6%D7%A8%D7%9B%D7%9F/"
    fetch_cpi_data(url)
