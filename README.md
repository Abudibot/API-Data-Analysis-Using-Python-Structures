# Day 1 - API Data Analysis Using Python Structures 
Fetches 10 customers from the JSONPlaceholder Users API with 'requests', flatten the nested address, geo and company objects into one row per customer, then analyse with plain Python (sets for unique cities, loops and dicts for counts). Results are saved with pandas and plotted with matplotlib.

## How to run 
''' 
python -m venv .venv 
source .venv/Scripts/activate 
pip install -r requirements.txt 
python analysis.py 
''' 
Outputs are written to the 'output/' folder

## Findings
- 10 customers were retrieved and all 10 live in different cities, so no city has more than one customer.
- The most common email domain is .biz; the other domains appear less often. 
- The chart shows how customers are spread across email domains. 

## Assumptions 
- The email domain means the part after the last dot (e.g biz, tv). 
- Ties for most common city are broken alphabetically. 
- The API is available and returns 10 records.