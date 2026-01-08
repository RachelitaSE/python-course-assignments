# Day 09 – Submission Report

This project analyzes course assignment submissions using the `day09/subjects.txt` file and the official deadlines defined in the main course README. It generates a report showing late submissions, missing submissions, submission-time distribution relative to deadlines, and the popularity of different assignment types.

The code is split into two parts: `Utilities.py` contains all reusable logic (data downloading, regex-based parsing, and datetime calculations), while `submission_report_gen.py` handles orchestration and reporting. The implementation uses **only Python’s standard library** and demonstrates practical use of regular expressions, datetime handling, and clean code separation.