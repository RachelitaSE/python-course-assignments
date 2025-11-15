# Consumer Price Index calculator

I wrote a Python app that calculates and prints the realitic value of an amount of money  linked to the consumer price index, helping you track the realistic value of your money. The code cpi_data.py uses the following url [cpi_data_web](https://mashcantaman.co.il/%D7%9E%D7%93%D7%93-%D7%94%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%9C%D7%A6%D7%A8%D7%9B%D7%9F/) to get the cpi of the last 20 years, and outputs an excel file that is easy to read.

Then cpi_calc.py is a python script that you can change the inputs in the script iself - it reads the cli_data.xlsx that cpi_data.py created. Input is : amount (in ILS), initial date, end date
Output : the realistic value of the money in ILS

The CLI code cpi_calc_cli.py should be used:

python cpi_calc_cli.py 
it prompts you interactively to enter the following- for example:
```
Enter Excel filename (default: cpi_data_fixed.xlsx): cpi_data.xlsx
Enter the amount to adjust (e.g., 10000): 1000
Enter start date (YYYY-MM-DD): 2013-08-09
Enter end date (YYYY-MM-DD): 2020-08-09
```
  Output:
```
============================
Original amount: 1,000.00 ILS
From: 2013-08-09
To:   2020-08-09
Adjusted (CPI): 979.47 ILS
============================
```
I used ChatGPT-5 to build all the versions.
The gui doesn't work for me as of now. I am still working on it. 

