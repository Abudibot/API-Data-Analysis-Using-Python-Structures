"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization 

- Fetch customers from the API
- Explore the nested JSON structure 
- Flatten each customer into one row 
- Analyse with plain Python structures 
- Print a short findings summary
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users" 
OUTPUT_DIR = Path("output")

# Fetch Data

def get_customers(url: str = API_URL) -> list[dict]:

    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)     # timeout stops it hanging forever
        response.raise_for_status()                  # raises on 404, 500, etc.
        return response.json()                       # list of customer dictionaries 
    except requests.exceptions.Timeout:
        print("Error: the request timed out.") 
    except requests.exceptions.ConnectionError:
        print("Error: could not connect. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: the server returned a bad status: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: request failed: {e}") 
    except ValueError:
        print("Error: the response was not valid JSON.") 
    return []                         # empty list lets the caller handle the failure gracefully 

# Explore the nested JSON structure 

def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items(): 
        print(" " * indent + f"{key}: {type(value).__name__}") 
        if isinstance(value, dict):       # nested object -> go one level deeper 
            explore(value, indent + 2) 

# Flatten each customer into one row

def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = [] 
    for c in customers: 
        address = c.get("address", {}) 
        geo = address.get("geo", {}) 
        email = c.get("email", "") 
        rows.append({ 
            "customer_id": c["id"], 
            "name": c["name"], 
            "username": c["username"], 
            "email": email, 
            "email_domain": email.rsplit(".", 1)[-1],   # 'biz' from 'a@b.biz' 
            "phone": c.get("phone"), 
            "city": address.get("city"), 
            "zipcode": address.get("zipcode"), 
            "latitude": float(geo["lat"]),           # API gives strings -> floats
            "longitude": float(geo["lng"]), 
            "company": c.get("company", {}).get("name"), 
            "website": c.get("website"),
        }) 
    return rows

# Analysis with plain Python structures (no pandas)

def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {c["city"] for c in customers}      # a set removes duplicates

def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {} 
    for c in customers: 
        city = c["city"] 
        counts[city] = counts.get(city, 0) + 1     # start at 0, add 1 each time 
    return counts 

def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    counts = {} 
    for c in customers: 
        tld = c["email_domain"] 
        counts[tld] = counts.get(tld, 0) + 1 
    return counts

# Saving results

def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)

def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    plt.figure(figsize=(8, 5)) 
    plt.bar(list(counts.keys()), list(counts.values())) 
    plt.title("Customers per Email Domain") 
    plt.xlabel("Email domain (TLD)") 
    plt.ylabel("Number of customers") 
    plt.xticks(rotation=45, ha="right")       # keeps tick labels readable
    plt.tight_layout() 
    plt.savefig(path) 
    plt.close() 


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True) 

    # 1. fetch 
    raw = get_customers() 
    if not raw: 
        raise SystemExit("No customers retrieved. Stopping.") 

    # 2. Explore the first record's structure 
    print("Structure of one customer record:") 
    explore(raw[0]) 
    print() 

    # 3. Flatten 
    rows = extract_attributes(raw) 

    # 4. Analyse 
    cities = city_counts(rows) 
    domains = email_domain_counts(rows) 
    # sort by count (high to low), then city name (A to Z) 
    ranked = sorted(cities.items(), key=lambda kv: (-kv[1], kv[0])) 

    # Save 
    to_dataframe(rows).to_csv(OUTPUT_DIR / "customers.csv", index=False)
    pd.DataFrame(ranked, columns=["city", "customer_count"]).to_csv(
        OUTPUT_DIR / "city_counts.csv", index=False
    ) 
    chart_path = OUTPUT_DIR / "customer_distribution.png" 
    plot_distribution(domains, chart_path) 

    # 6. Findings summary 
    top_city, top_count = ranked[0] 
    print(f"Customers retrieved : {len(rows)}") 
    print(f"Unique cities       : {len(unique_cities(rows))}") 
    print(f"Most common city    : {top_city} ({top_count})") 
    print(f"Email domains       : {domains}") 
    print(f"Chart saved to      : {chart_path.as_posix()}")
