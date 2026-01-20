# Day 09 – Submission Report

This project analyzes assignment submission data from the course GitHub repository. It downloads the main `README.md` to extract the official assignment deadlines and downloads `day09/subjects.txt` to read all submission records. Using this data, the code determines which students submitted each assignment, when they submitted it, and whether the submission was on time or late.

## What the code does
The program generates a textual report that includes:
1. Students who submitted assignments **after the deadline**, including how late they were  
2. Students who **did not submit** specific assignments  
3. A **distribution of submission times** relative to the deadlines  
4. The **popularity** of each assignment type  

## How the code is built
The logic is separated into two files:

- `Utilities.py`  
  Handles data retrieval, parsing (using regular expressions), and time calculations.

- `submission_report_gen.py`  
  The main script that should be executed. It performs data aggregation and generates the final report.

## Libraries to install
The code uses **only Python’s standard library**. No external libraries are required.

