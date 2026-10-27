# Day 1 - API Data Analysis Using Python Structures 
Fetches 10 customers from the JSONPlaceholder Users API, flattens the nested data, analyses it with plain Python (lists, dicts, sets, loops), and saves CSVs and a chart. 

## What it produces 
- 'output/customers.csv': one flat row per customer 
- 'output/city_counts.csv': customers per city (sorted by count, then city) 
- 'output/customer_distributiony.png': bar chart of customers per email domain 
- 'Console findings: customers retrieved, unique cities, most common city, email domains 

## How to run 
''' 
python -m venv .venv 
source .venv/Scripts/activate 
pip install -r requirements.txt 
python starter.py 
''' 

## Tools 
Python, requests, pandas, matplotlib